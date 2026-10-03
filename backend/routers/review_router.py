from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.user import User
from repository import review_repo
from routers._common import ensure_competitor, get_or_404
from schemas.review_schema import ReviewCreate, ReviewRead
from security.deps import get_current_user, require_role

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.get("", response_model=List[ReviewRead])
def list_reviews(
    competitor_id: Optional[int] = None,
    sentiment: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return review_repo.list_all(
        db, user.company_id, skip=skip, limit=limit, competitor_id=competitor_id, sentiment=sentiment
    )


@router.post("", response_model=ReviewRead, status_code=201)
def create_review(
    payload: ReviewCreate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    ensure_competitor(db, user.company_id, payload.competitor_id)
    return review_repo.create(db, user.company_id, payload.model_dump())


@router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    review = get_or_404(review_repo, db, user.company_id, review_id, "Review")
    review_repo.delete(db, review)
    return Response(status_code=204)