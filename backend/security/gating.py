from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.clock import utcnow
from core.constants import PLAN_LIMITS
from database import get_db
from models.company import Company
from models.competitor import Competitor
from models.research_usage import ResearchUsage
from models.user import User
from security.deps import get_current_user
from models.subscription import Subscription


def require_active_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Blocks any request if the trial has expired and there's no active paid plan."""
    company = db.get(Company, user.company_id)
    if company is None:
        raise HTTPException(status_code=403, detail="Company not found")

    if company.subscription_status == "active":
        sub = db.scalar(select(Subscription).where(Subscription.company_id == company.id))
        if sub and sub.provider == "mpesa" and sub.current_period_end and sub.current_period_end < utcnow():
            sub.status = "expired"
            company.subscription_status = "expired"
            db.commit()
            raise HTTPException(
                status_code=402,
                detail="Your M-Pesa subscription period has ended. Please renew to continue.",
            )
        return user

    if company.subscription_status == "trialing":
        if company.trial_ends_at and company.trial_ends_at < utcnow():
            raise HTTPException(
                status_code=402,
                detail="Your free trial has ended. Please subscribe to continue using VERIDEX.",
            )
        return user

    raise HTTPException(
        status_code=402,
        detail="Your subscription is not active. Please subscribe or renew to continue.",
    )


def enforce_competitor_limit(
    user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
) -> User:
    """Blocks adding a new competitor if the plan's limit is already reached. Unlimited plans skip this."""
    company = db.get(Company, user.company_id)
    limits = PLAN_LIMITS.get(company.plan, PLAN_LIMITS["trial"])
    max_competitors = limits.get("max_competitors")

    if max_competitors is not None:
        current_count = db.scalar(
            select(func.count()).select_from(Competitor).where(Competitor.company_id == user.company_id)
        ) or 0
        if current_count >= max_competitors:
            raise HTTPException(
                status_code=402,
                detail=f"Your {company.plan} plan allows up to {max_competitors} competitors. "
                       f"Upgrade your plan to track more.",
            )
    return user


def enforce_research_limit(
    user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
) -> User:
    """Blocks a research run once the plan's research quota is used up. Unlimited plans skip this."""
    company = db.get(Company, user.company_id)
    limits = PLAN_LIMITS.get(company.plan, PLAN_LIMITS["trial"])
    max_runs = limits.get("max_research_runs")

    if max_runs is not None:
        count = db.scalar(
            select(func.count()).select_from(ResearchUsage).where(ResearchUsage.company_id == user.company_id)
        ) or 0
        if count >= max_runs:
            raise HTTPException(
                status_code=402,
                detail=f"You've used all {max_runs} research runs on your {company.plan} plan. Upgrade to run more.",
            )
    return user