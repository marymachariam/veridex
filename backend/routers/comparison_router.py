from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.insight import CompetitorInsight
from models.user import User
from repository import competitor_repo, feature_repo, pricing_repo
from routers._common import get_or_404
from schemas.comparison_schema import CompetitorComparisonEntry, ComparisonRequest, ComparisonResponse
from security.deps import get_current_user

router = APIRouter(prefix="/api/v1/comparison", tags=["comparison"])


@router.post("", response_model=ComparisonResponse)
def compare_competitors(
    payload: ComparisonRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entries = []
    for competitor_id in payload.competitor_ids:
        competitor = get_or_404(competitor_repo, db, user.company_id, competitor_id, "Competitor")
        insight = db.scalar(
            select(CompetitorInsight).where(
                CompetitorInsight.company_id == user.company_id,
                CompetitorInsight.competitor_id == competitor_id,
            )
        )
        entries.append(
            CompetitorComparisonEntry(
                competitor=competitor,
                pricing=pricing_repo.list_all(db, user.company_id, competitor_id=competitor_id, limit=50),
                features=feature_repo.list_all(db, user.company_id, competitor_id=competitor_id, limit=100),
                insight=insight,
            )
        )
    return ComparisonResponse(competitors=entries)