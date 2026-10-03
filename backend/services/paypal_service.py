import logging
from typing import Optional

import requests

from core.config import settings

logger = logging.getLogger("veridex.paypal")


def _get_access_token() -> str:
    resp = requests.post(
        f"{settings.paypal_base_url}/v1/oauth2/token",
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def create_product_and_plan(plan_name: str, price_usd: float) -> str:
    """One-time setup helper: creates a PayPal billing plan and returns its plan_id.
    Run this once per plan tier and hardcode the returned plan_id (see Step below)."""
    token = _get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    product_resp = requests.post(
        f"{settings.paypal_base_url}/v1/catalogs/products",
        headers=headers,
        json={"name": f"VERIDEX {plan_name}", "type": "SERVICE", "category": "SOFTWARE"},
        timeout=15,
    )
    product_resp.raise_for_status()
    product_id = product_resp.json()["id"]

    plan_resp = requests.post(
        f"{settings.paypal_base_url}/v1/billing/plans",
        headers=headers,
        json={
            "product_id": product_id,
            "name": f"VERIDEX {plan_name} Monthly",
            "billing_cycles": [{
                "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,  # 0 = infinite, renews until cancelled
                "pricing_scheme": {"fixed_price": {"value": str(price_usd), "currency_code": "USD"}},
            }],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "payment_failure_threshold": 2,
            },
        },
        timeout=15,
    )
    plan_resp.raise_for_status()
    return plan_resp.json()["id"]


def create_subscription(plan_id: str, return_url: str, cancel_url: str) -> dict:
    """Returns the subscription object; caller redirects the user to the 'approve' link inside it."""
    token = _get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    resp = requests.post(
        f"{settings.paypal_base_url}/v1/billing/subscriptions",
        headers=headers,
        json={
            "plan_id": plan_id,
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "user_action": "SUBSCRIBE_NOW",
            },
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_subscription(subscription_id: str) -> dict:
    token = _get_access_token()
    resp = requests.get(
        f"{settings.paypal_base_url}/v1/billing/subscriptions/{subscription_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def cancel_subscription(subscription_id: str, reason: str = "User requested cancellation") -> None:
    token = _get_access_token()
    requests.post(
        f"{settings.paypal_base_url}/v1/billing/subscriptions/{subscription_id}/cancel",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"reason": reason},
        timeout=15,
    ).raise_for_status()
    
def verify_webhook_signature(headers, event: dict) -> bool:
    token = _get_access_token()
    resp = requests.post(
        f"{settings.paypal_base_url}/v1/notifications/verify-webhook-signature",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "auth_algo": headers.get("paypal-auth-algo"),
            "cert_url": headers.get("paypal-cert-url"),
            "transmission_id": headers.get("paypal-transmission-id"),
            "transmission_sig": headers.get("paypal-transmission-sig"),
            "transmission_time": headers.get("paypal-transmission-time"),
            "webhook_id": settings.PAYPAL_WEBHOOK_ID,
            "webhook_event": event,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("verification_status") == "SUCCESS"