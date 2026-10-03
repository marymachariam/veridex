from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.user import User
from repository import pricing_repo
from routers._common import ensure_competitor, get_or_404
from schemas.pricing_schema import PricingCreate, PricingRead, PricingUpdate
from security.deps import get_current_user, require_role

router = APIRouter(prefix="/api/v1/pricing", tags=["pricing"])

NULLABLE_FIELDS = {"price_usd", "description"}


@router.get("", response_model=List[PricingRead])
def list_pricing(
    competitor_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return pricing_repo.list_all(db, user.company_id, skip=skip, limit=limit, competitor_id=competitor_id)


@router.post("", response_model=PricingRead, status_code=201)
def create_pricing(
    payload: PricingCreate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    ensure_competitor(db, user.company_id, payload.competitor_id)
    return pricing_repo.create(db, user.company_id, payload.model_dump())


@router.put("/{pricing_id}", response_model=PricingRead)
def update_pricing(
    pricing_id: int,
    payload: PricingUpdate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    tier = get_or_404(pricing_repo, db, user.company_id, pricing_id, "Pricing tier")
    data = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None or k in NULLABLE_FIELDS}
    return pricing_repo.update(db, tier, data)


@router.delete("/{pricing_id}", status_code=204)
def delete_pricing(
    pricing_id: int,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    tier = get_or_404(pricing_repo, db, user.company_id, pricing_id, "Pricing tier")
    pricing_repo.delete(db, tier)
    return Response(status_code=204)