from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models.competitor import Competitor
from models.price_history import PriceHistory
from models.pricing import Pricing
from models.review import Review
from models.user import User
from repository import price_history_repo
from schemas.price_history_schema import PriceHistoryRead
from security.deps import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


class DashboardSummary(BaseModel):
    competitors: int
    pricing_tiers: int
    reviews: int
    avg_rating: Optional[float] = None
    sentiment: Dict[str, int]
    recent_price_changes: List[PriceHistoryRead]


def _count(db: Session, model, company_id: int) -> int:
    return db.scalar(select(func.count()).select_from(model).where(model.company_id == company_id)) or 0


@router.get("/summary", response_model=DashboardSummary)
def summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cid = user.company_id

    avg = db.scalar(select(func.avg(Review.rating)).where(Review.company_id == cid))
    sentiment = {"positive": 0, "neutral": 0, "negative": 0}
    rows = db.execute(
        select(Review.sentiment, func.count()).where(Review.company_id == cid).group_by(Review.sentiment)
    ).all()
    for label, total in rows:
        sentiment[label] = total

    return DashboardSummary(
        competitors=_count(db, Competitor, cid),
        pricing_tiers=_count(db, Pricing, cid),
        reviews=_count(db, Review, cid),
        avg_rating=round(float(avg), 2) if avg is not None else None,
        sentiment=sentiment,
        recent_price_changes=[
            PriceHistoryRead.model_validate(row) for row in price_history_repo.list_all(db, cid, limit=5)
        ],
    )