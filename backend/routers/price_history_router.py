from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.user import User
from repository import price_history_repo
from routers._common import ensure_competitor, get_or_404
from schemas.price_history_schema import PriceHistoryCreate, PriceHistoryRead
from security.deps import get_current_user, require_role

router = APIRouter(prefix="/api/v1/price-history", tags=["price-history"])


@router.get("", response_model=List[PriceHistoryRead])
def list_price_history(
    competitor_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return price_history_repo.list_all(db, user.company_id, skip=skip, limit=limit, competitor_id=competitor_id)


@router.post("", response_model=PriceHistoryRead, status_code=201)
def create_price_change(
    payload: PriceHistoryCreate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    ensure_competitor(db, user.company_id, payload.competitor_id)
    data = payload.model_dump()
    if data.get("change_date") is None:
        data.pop("change_date", None)
    return price_history_repo.create(db, user.company_id, data)


@router.delete("/{history_id}", status_code=204)
def delete_price_change(
    history_id: int,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    entry = get_or_404(price_history_repo, db, user.company_id, history_id, "Price change")
    price_history_repo.delete(db, entry)
    return Response(status_code=204)