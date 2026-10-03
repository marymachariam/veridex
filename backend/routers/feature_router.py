from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.user import User
from repository import feature_repo
from routers._common import ensure_competitor, get_or_404
from schemas.feature_schema import FeatureCreate, FeatureRead
from security.deps import get_current_user, require_role

router = APIRouter(prefix="/api/v1/features", tags=["features"])


@router.get("", response_model=List[FeatureRead])
def list_features(
    competitor_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return feature_repo.list_all(db, user.company_id, skip=skip, limit=limit, competitor_id=competitor_id)


@router.post("", response_model=FeatureRead, status_code=201)
def create_feature(
    payload: FeatureCreate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    ensure_competitor(db, user.company_id, payload.competitor_id)
    return feature_repo.create(db, user.company_id, payload.model_dump())


@router.delete("/{feature_id}", status_code=204)
def delete_feature(
    feature_id: int,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    feature = get_or_404(feature_repo, db, user.company_id, feature_id, "Feature")
    feature_repo.delete(db, feature)
    return Response(status_code=204)