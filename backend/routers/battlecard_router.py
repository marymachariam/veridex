import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.insight import CompetitorInsight
from models.user import User
from repository import competitor_repo, feature_repo, pricing_repo
from routers._common import get_or_404
from schemas.battlecard_schema import BattlecardRead
from security.deps import get_current_user
from services.battlecard_service import generate_battlecard

logger = logging.getLogger("veridex.battlecard")
router = APIRouter(prefix="/api/v1/battlecard", tags=["battlecard"])


@router.get("/{competitor_id}", response_model=BattlecardRead)
def get_battlecard(competitor_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    competitor = get_or_404(competitor_repo, db, user.company_id, competitor_id, "Competitor")
    pricing = pricing_repo.list_all(db, user.company_id, competitor_id=competitor_id, limit=50)
    features = feature_repo.list_all(db, user.company_id, competitor_id=competitor_id, limit=100)
    insight = db.scalar(
        select(CompetitorInsight).where(
            CompetitorInsight.company_id == user.company_id, CompetitorInsight.competitor_id == competitor_id
        )
    )

    pricing_data = [{"tier_name": p.tier_name, "price_usd": p.price_usd, "billing_period": p.billing_period} for p in pricing]
    feature_data = [f.feature_name for f in features]
    insight_data = {
        "tagline": insight.tagline if insight else None,
        "summary": insight.summary if insight else None,
        "strengths": insight.strengths if insight else None,
        "weaknesses": insight.weaknesses if insight else None,
    } if insight else {}

    try:
        result = generate_battlecard(competitor.name, pricing_data, feature_data, insight_data)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception:
        logger.exception("Battlecard generation failed for competitor_id=%s", competitor_id)
        raise HTTPException(status_code=502, detail="Battlecard generation failed. Please try again.")

    return BattlecardRead(
        competitor_id=competitor.id,
        competitor_name=competitor.name,
        one_liner=result.get("one_liner", ""),
        why_we_win=result.get("why_we_win", []),
        watch_out_for=result.get("watch_out_for", []),
        objection_handling=result.get("objection_handling", []),
        pricing_summary=result.get("pricing_summary", ""),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )