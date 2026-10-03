from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.research_history import ResearchHistory
from models.user import User
from schemas.history_schema import HistoryDetail, HistoryItem
from security.deps import get_current_user, require_role

router = APIRouter(prefix="/api/v1/history", tags=["history"])


def _full_name(first: Optional[str], last: Optional[str]) -> Optional[str]:
    return " ".join(p for p in [first, last] if p) or None


@router.get("", response_model=List[HistoryItem])
def list_history(
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(ResearchHistory, User.first_name, User.last_name)
        .outerjoin(User, User.id == ResearchHistory.user_id)
        .where(ResearchHistory.company_id == user.company_id)
        .order_by(ResearchHistory.created_at.desc(), ResearchHistory.id.desc())
        .limit(limit)
        .offset(offset)
    )
    if search and search.strip():
        stmt = stmt.where(ResearchHistory.competitor_name.ilike(f"%{search.strip()}%"))

    items = []
    for h, first, last in db.execute(stmt).all():
        insight = (h.result or {}).get("insight") or {}
        items.append(HistoryItem(
            id=h.id,
            competitor_id=h.competitor_id,
            competitor_name=h.competitor_name,
            website=h.website,
            category=h.category,
            created_at=h.created_at,
            run_by=_full_name(first, last),
            summary=insight.get("summary"),
        ))
    return items


@router.get("/{history_id}", response_model=HistoryDetail)
def get_history_item(
    history_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.execute(
        select(ResearchHistory, User.first_name, User.last_name)
        .outerjoin(User, User.id == ResearchHistory.user_id)
        .where(ResearchHistory.id == history_id, ResearchHistory.company_id == user.company_id)
    ).first()
    if row is None:
        raise HTTPException(status_code=404, detail="History entry not found")

    h, first, last = row
    return HistoryDetail(
        id=h.id,
        competitor_id=h.competitor_id,
        competitor_name=h.competitor_name,
        website=h.website,
        category=h.category,
        created_at=h.created_at,
        run_by=_full_name(first, last),
        result=h.result,
    )


@router.delete("/{history_id}", status_code=204)
def delete_history_item(
    history_id: int,
    user: User = Depends(require_role(UserRole.ANALYST)),
    db: Session = Depends(get_db),
):
    h = db.scalar(
        select(ResearchHistory).where(ResearchHistory.id == history_id, ResearchHistory.company_id == user.company_id)
    )
    if h is None:
        raise HTTPException(status_code=404, detail="History entry not found")
    db.delete(h)
    db.commit()
    return Response(status_code=204)