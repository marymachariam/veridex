from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.competitor import Competitor
from models.user import User
from repository import competitor_repo
from routers._common import get_or_404
from schemas.competitor_schema import CompetitorCreate, CompetitorRead, CompetitorUpdate
from security.deps import get_current_user, require_role
from security.gating import enforce_competitor_limit

router = APIRouter(prefix="/api/v1/competitors", tags=["competitors"])


def _name_taken(db: Session, company_id: int, name: str, exclude_id: int = None) -> bool:
    stmt = select(Competitor.id).where(
        Competitor.company_id == company_id, func.lower(Competitor.name) == name.lower()
    )
    if exclude_id is not None:
        stmt = stmt.where(Competitor.id != exclude_id)
    return db.scalar(stmt) is not None


@router.get("", response_model=List[CompetitorRead])
def list_competitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return competitor_repo.list_all(db, user.company_id, skip=skip, limit=limit)


@router.post("", response_model=CompetitorRead, status_code=201)
def create_competitor(
    payload: CompetitorCreate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    _gate: User = Depends(enforce_competitor_limit),
    db: Session = Depends(get_db),
):
    if _name_taken(db, user.company_id, payload.name):
        raise HTTPException(status_code=409, detail="You are already tracking a competitor with this name")
    try:
        return competitor_repo.create(db, user.company_id, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You are already tracking a competitor with this name")


@router.get("/{competitor_id}", response_model=CompetitorRead)
def get_competitor(competitor_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_or_404(competitor_repo, db, user.company_id, competitor_id, "Competitor")


@router.put("/{competitor_id}", response_model=CompetitorRead)
def update_competitor(
    competitor_id: int,
    payload: CompetitorUpdate,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    competitor = get_or_404(competitor_repo, db, user.company_id, competitor_id, "Competitor")
    data = payload.model_dump(exclude_unset=True)
    if data.get("name") is None:
        data.pop("name", None)
    elif _name_taken(db, user.company_id, data["name"], exclude_id=competitor_id):
        raise HTTPException(status_code=409, detail="You are already tracking a competitor with this name")
    return competitor_repo.update(db, competitor, data)


@router.delete("/{competitor_id}", status_code=204)
def delete_competitor(
    competitor_id: int,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    competitor = get_or_404(competitor_repo, db, user.company_id, competitor_id, "Competitor")
    competitor_repo.delete(db, competitor)
    return Response(status_code=204)