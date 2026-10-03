from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import competitor_repo


def get_or_404(repo, db: Session, company_id: int, obj_id: int, label: str = "Resource"):
    obj = repo.get(db, company_id, obj_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return obj


def ensure_competitor(db: Session, company_id: int, competitor_id: int):
    """Guarantees the competitor exists AND belongs to the caller's company."""
    return get_or_404(competitor_repo, db, company_id, competitor_id, "Competitor")