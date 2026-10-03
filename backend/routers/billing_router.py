import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
import secrets

from core.clock import utcnow
from core.config import settings
from core.constants import PAYPAL_PLAN_IDS, PLAN_PRICES_KES, PLAN_PRICES_USD, UserRole
from database import get_db
from models.company import Company
from models.payment import Payment
from models.subscription import Subscription
from models.user import User
from schemas.billing_schema import (
    MpesaStkRequest,
    MpesaStkResponse,
    SubscribeRequest,
    SubscribeResponse,
    SubscriptionStatusRead,
)
from security.deps import get_current_user, require_role
from services.mpesa_service import normalize_phone, stk_push
from services.paypal_service import cancel_subscription, create_subscription, get_subscription, verify_webhook_signature

logger = logging.getLogger("veridex.billing")
router = APIRouter(prefix="/api/v1/billing", tags=["billing"])


def _get_or_create_subscription(db: Session, company_id: int) -> Subscription:
    sub = db.scalar(select(Subscription).where(Subscription.company_id == company_id))
    if sub is None:
        sub = Subscription(company_id=company_id, plan="trial", status="trialing")
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return sub


@router.get("/status", response_model=SubscriptionStatusRead)
def billing_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub = _get_or_create_subscription(db, user.company_id)
    return SubscriptionStatusRead(
        plan=sub.plan,
        status=sub.status,
        provider=sub.provider,
        current_period_end=sub.current_period_end.isoformat() if sub.current_period_end else None,
    )


# ---------------------------------------------------------------------------
# PayPal
# ---------------------------------------------------------------------------

@router.post("/paypal/subscribe", response_model=SubscribeResponse)
def paypal_subscribe(
    payload: SubscribeRequest,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    if payload.plan not in PAYPAL_PLAN_IDS:
        raise HTTPException(status_code=400, detail="Unknown plan")

    plan_id = PAYPAL_PLAN_IDS[payload.plan]
    frontend = settings.FRONTEND_URL or "http://localhost:8501"

    try:
        result = create_subscription(
            plan_id=plan_id,
            return_url=f"{frontend}/Billing?paypal_status=success",
            cancel_url=f"{frontend}/Billing?paypal_status=cancelled",
        )
    except Exception:
        logger.exception("PayPal subscription creation failed for company_id=%s", user.company_id)
        raise HTTPException(status_code=502, detail="Could not start PayPal checkout. Please try again.")

    approval_url = next((link["href"] for link in result.get("links", []) if link["rel"] == "approve"), None)
    if not approval_url:
        raise HTTPException(status_code=502, detail="PayPal did not return an approval link.")

    sub = _get_or_create_subscription(db, user.company_id)
    sub.paypal_subscription_id = result["id"]
    sub.provider = "paypal"
    db.commit()

    payment = Payment(
        company_id=user.company_id,
        provider="paypal",
        plan=payload.plan,
        amount=PLAN_PRICES_USD.get(payload.plan, 0),
        currency="USD",
        status="pending",
        provider_reference=result["id"],
    )
    db.add(payment)
    db.commit()

    return SubscribeResponse(approval_url=approval_url, subscription_id=result["id"])


@router.post("/paypal/cancel")
def paypal_cancel(user: User = Depends(require_role(UserRole.ADMIN)), db: Session = Depends(get_db)):
    sub = _get_or_create_subscription(db, user.company_id)
    if not sub.paypal_subscription_id:
        raise HTTPException(status_code=400, detail="No active PayPal subscription found")

    try:
        cancel_subscription(sub.paypal_subscription_id)
    except Exception:
        logger.exception("PayPal cancellation failed for company_id=%s", user.company_id)
        raise HTTPException(status_code=502, detail="Could not cancel with PayPal. Please try again.")

    sub.status = "cancelled"
    db.commit()
    return {"status": "cancelled"}


@router.post("/paypal/webhook")
async def paypal_webhook(request: Request, db: Session = Depends(get_db)):
    event = await request.json()
    try:
        verified = verify_webhook_signature(request.headers, event)
    except Exception:
        logger.exception("PayPal webhook verification call failed")
        raise HTTPException(status_code=400, detail="Could not verify webhook")
    if not verified:
        logger.warning("PayPal webhook with invalid signature rejected")
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event.get("event_type", "")
    resource = event.get("resource", {})
    event_type = event.get("event_type", "")
    resource = event.get("resource", {})

    logger.info("PayPal webhook received: %s", event_type)

    subscription_id = resource.get("id") if "SUBSCRIPTION" in event_type else resource.get("billing_agreement_id")
    if not subscription_id:
        return {"status": "ignored"}

    sub = db.scalar(select(Subscription).where(Subscription.paypal_subscription_id == subscription_id))
    if sub is None:
        logger.warning("Webhook for unknown subscription_id=%s", subscription_id)
        return {"status": "ignored"}

    if event_type in ("BILLING.SUBSCRIPTION.ACTIVATED", "PAYMENT.SALE.COMPLETED"):
        try:
            details = get_subscription(subscription_id)
            plan_id = details.get("plan_id")
            plan_name = next((name for name, pid in PAYPAL_PLAN_IDS.items() if pid == plan_id), sub.plan)
        except Exception:
            plan_name = sub.plan

        sub.status = "active"
        sub.plan = plan_name
        db.commit()

        company = db.get(Company, sub.company_id)
        if company:
            company.plan = plan_name
            company.subscription_status = "active"
            db.commit()

        payment = db.scalar(
            select(Payment).where(Payment.provider_reference == subscription_id, Payment.status == "pending")
        )
        if payment:
            payment.status = "completed"
            payment.completed_at = utcnow()
            db.commit()

    elif event_type in ("BILLING.SUBSCRIPTION.CANCELLED", "BILLING.SUBSCRIPTION.SUSPENDED"):
        sub.status = "cancelled"
        db.commit()
        company = db.get(Company, sub.company_id)
        if company:
            company.subscription_status = "cancelled"
            db.commit()

    elif event_type == "BILLING.SUBSCRIPTION.PAYMENT.FAILED":
        sub.status = "past_due"
        db.commit()

    return {"status": "processed"}


# ---------------------------------------------------------------------------
# M-Pesa
# ---------------------------------------------------------------------------

@router.post("/mpesa/stk-push", response_model=MpesaStkResponse)
def mpesa_stk_push(
    payload: MpesaStkRequest,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    if payload.plan not in PLAN_PRICES_KES:
        raise HTTPException(status_code=400, detail="Unknown plan")

    phone = normalize_phone(payload.phone_number)
    if not phone.startswith("254") or len(phone) != 12:
        raise HTTPException(status_code=400, detail="Enter a valid Kenyan phone number, e.g. 0712345678")

    amount = int(PLAN_PRICES_KES[payload.plan])

    try:
        result = stk_push(
            phone_number=phone,
            amount=amount,
            account_reference=f"VERIDEX-{user.company_id}",
            description=f"VERIDEX {payload.plan}",
        )
    except Exception:
        logger.exception("M-Pesa STK push failed for company_id=%s", user.company_id)
        raise HTTPException(status_code=502, detail="Could not start M-Pesa payment. Please try again.")

    if result.get("ResponseCode") != "0":
        raise HTTPException(status_code=502, detail=result.get("ResponseDescription", "M-Pesa request failed"))

    checkout_request_id = result["CheckoutRequestID"]

    payment = Payment(
        company_id=user.company_id,
        provider="mpesa",
        plan=payload.plan,
        amount=amount,
        currency="KES",
        status="pending",
        provider_reference=checkout_request_id,
    )
    db.add(payment)
    db.commit()

    return MpesaStkResponse(
        checkout_request_id=checkout_request_id,
        message="Check your phone and enter your M-Pesa PIN to complete payment.",
    )


@router.post("/stk-callback/{secret}")
async def stk_callback(secret: str, request: Request, db: Session = Depends(get_db)):
    """Safaricom calls this after the customer enters their PIN (or cancels/times out).
    The secret in the URL path stops anyone else from calling it."""
    if not settings.MPESA_CALLBACK_SECRET or not secrets.compare_digest(secret, settings.MPESA_CALLBACK_SECRET):
        raise HTTPException(status_code=404, detail="Not found")

    body = await request.json()
    logger.info("STK callback received: %s", body)

    callback = body.get("Body", {}).get("stkCallback", {})
    checkout_request_id = callback.get("CheckoutRequestID")
    result_code = callback.get("ResultCode")

    if not checkout_request_id:
        return {"status": "ignored"}

    payment = db.scalar(select(Payment).where(Payment.provider_reference == checkout_request_id))
    if payment is None:
        logger.warning("Callback for unknown CheckoutRequestID=%s", checkout_request_id)
        return {"status": "ignored"}

    if payment.status == "completed":  # Safaricom can retry; never process twice
        return {"status": "already_processed"}

    if result_code == 0:
        items = callback.get("CallbackMetadata", {}).get("Item", [])
        receipt = next((i.get("Value") for i in items if i.get("Name") == "MpesaReceiptNumber"), None)
        paid_amount = next((i.get("Value") for i in items if i.get("Name") == "Amount"), None)

        if paid_amount is None or float(paid_amount) < float(payment.amount):
            logger.error("Amount mismatch for %s: paid=%s expected=%s", checkout_request_id, paid_amount, payment.amount)
            payment.status = "failed"
            db.commit()
            return {"status": "amount_mismatch"}

        payment.status = "completed"
        payment.completed_at = utcnow()
        payment.mpesa_receipt_number = str(receipt) if receipt else None
        db.commit()

        sub = _get_or_create_subscription(db, payment.company_id)
        start_from = sub.current_period_end if sub.current_period_end and sub.current_period_end > utcnow() else utcnow()
        sub.plan = payment.plan
        sub.provider = "mpesa"
        sub.status = "active"
        sub.current_period_end = start_from + timedelta(days=30)
        db.commit()

        company = db.get(Company, payment.company_id)
        if company:
            company.plan = payment.plan
            company.subscription_status = "active"
            db.commit()
    else:
        payment.status = "failed"
        db.commit()

    return {"status": "processed"}