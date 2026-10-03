from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from repository import change_log_repo
from routers._common import get_or_404
from schemas.change_log_schema import ChangeLogRead
from security.deps import get_current_user

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.get("", response_model=List[ChangeLogRead])
def list_alerts(
    competitor_id: Optional[int] = None,
    unread_only: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    filters = {"competitor_id": competitor_id}
    if unread_only:
        filters["is_read"] = 0
    return change_log_repo.list_all(db, user.company_id, skip=skip, limit=limit, **filters)


@router.post("/{alert_id}/mark-read", response_model=ChangeLogRead)
def mark_alert_read(alert_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    alert = get_or_404(change_log_repo, db, user.company_id, alert_id, "Alert")
    return change_log_repo.update(db, alert, {"is_read": 1})


@router.post("/mark-all-read")
def mark_all_read(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    unread = change_log_repo.list_all(db, user.company_id, is_read=0, limit=1000)
    for alert in unread:
        change_log_repo.update(db, alert, {"is_read": 1})
    return {"marked_read": len(unread)}