import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.competitor import Competitor
from models.insight import CompetitorInsight
from models.research_usage import ResearchUsage
from models.user import User
from repository import change_log_repo, competitor_repo, feature_repo, insight_repo, pricing_repo, review_repo
from schemas.research_schema import ResearchReport, ResearchRequest
from security.deps import get_current_user, require_role
from security.gating import enforce_research_limit
from services.change_detection_service import diff_features, diff_positioning, diff_pricing
from services.research_service import research_competitor
from models.research_history import ResearchHistory

logger = logging.getLogger("veridex.research")
router = APIRouter(prefix="/api/v1/research", tags=["research"])


def _run_research_and_diff(db: Session, company_id: int, name: str, website: str = None, category: str = None):
    """Core research logic, shared by the manual endpoint and the scheduled background job."""
    data = research_competitor(name, website, category)

    competitor = db.scalar(
        select(Competitor).where(Competitor.company_id == company_id, Competitor.name.ilike(name))
    )
    result_website = data.get("website") or website
    founded_year = data.get("founded_year")
    result_category = data.get("category") or category or "Other"
    is_first_run = competitor is None

    old_pricing, old_features, old_tagline = [], [], None
    if competitor is not None:
        old_pricing = [
            {"tier_name": p.tier_name, "price_usd": p.price_usd, "billing_period": p.billing_period}
            for p in pricing_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500)
        ]
        old_features = [
            f.feature_name for f in feature_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500)
        ]
        existing_insight = db.scalar(select(CompetitorInsight).where(CompetitorInsight.competitor_id == competitor.id))
        old_tagline = existing_insight.tagline if existing_insight else None

    if competitor is None:
        competitor = competitor_repo.create(
            db, company_id,
            {"name": name, "category": result_category, "website": result_website, "founded_year": founded_year},
        )
    else:
        update_data = {"category": result_category}
        if result_website:
            update_data["website"] = result_website
        if founded_year:
            update_data["founded_year"] = founded_year
        competitor = competitor_repo.update(db, competitor, update_data)

    for old in pricing_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500):
        pricing_repo.delete(db, old)
    for old in feature_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500):
        feature_repo.delete(db, old)

    for tier in data.get("pricing", [])[:20]:
        if not tier.get("tier_name"):
            continue
        pricing_repo.create(db, company_id, {
            "competitor_id": competitor.id,
            "tier_name": tier["tier_name"][:100],
            "price_usd": tier.get("price_usd"),
            "billing_period": tier.get("billing_period", "monthly"),
            "description": tier.get("description"),
        })

    for feat in data.get("features", [])[:30]:
        if not feat.get("feature_name"):
            continue
        feature_repo.create(db, company_id, {
            "competitor_id": competitor.id,
            "feature_name": feat["feature_name"][:255],
            "tier_available": feat.get("tier_available"),
        })

    insight = db.scalar(select(CompetitorInsight).where(CompetitorInsight.competitor_id == competitor.id))
    insight_data = {
        "tagline": data.get("tagline"),
        "target_market": data.get("target_market"),
        "summary": data.get("summary"),
        "strengths": "\n".join(data.get("strengths", [])),
        "weaknesses": "\n".join(data.get("weaknesses", [])),
        "opportunities": "\n".join(data.get("opportunities", [])),
        "threats": "\n".join(data.get("threats", [])),
        "recent_signals": "\n".join(data.get("recent_signals", [])),
        "sources": "\n".join(data.get("sources", [])),
    }
    if insight is None:
        insight = insight_repo.create(db, company_id, {**insight_data, "competitor_id": competitor.id})
    else:
        insight = insight_repo.update(db, insight, insight_data)

    # Auto-populate sentiment from the SWOT the research already produced (no separate scrape needed).
    for old_review in review_repo.list_all(db, company_id, competitor_id=competitor.id, limit=50):
        review_repo.delete(db, old_review)

    for strength in data.get("strengths", [])[:5]:
        review_repo.create(db, company_id, {
            "competitor_id": competitor.id,
            "source": "AI Analysis",
            "rating": 4.5,
            "sentiment": "positive",
            "comment_summary": strength,
        })
    for weakness in data.get("weaknesses", [])[:5]:
        review_repo.create(db, company_id, {
            "competitor_id": competitor.id,
            "source": "AI Analysis",
            "rating": 2.0,
            "sentiment": "negative",
            "comment_summary": weakness,
        })

    if not is_first_run:
        new_pricing = [
            {"tier_name": t.get("tier_name"), "price_usd": t.get("price_usd"), "billing_period": t.get("billing_period", "monthly")}
            for t in data.get("pricing", []) if t.get("tier_name")
        ]
        new_features = [f.get("feature_name") for f in data.get("features", []) if f.get("feature_name")]

        all_changes = (
            diff_pricing(old_pricing, new_pricing)
            + diff_features(old_features, new_features)
            + diff_positioning(old_tagline, data.get("tagline"))
        )
        for change in all_changes:
            change_log_repo.create(db, company_id, {**change, "competitor_id": competitor.id})

    db.refresh(competitor)
    return competitor, pricing_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500), \
        feature_repo.list_all(db, company_id, competitor_id=competitor.id, limit=500), insight


@router.post("/competitor", response_model=ResearchReport)
def run_competitor_research(
    payload: ResearchRequest,
    user: User = Depends(require_role(UserRole.ANALYST)),
    _gate: User = Depends(enforce_research_limit),
    db: Session = Depends(get_db),
):
    try:
        competitor, pricing, features, insight = _run_research_and_diff(
            db, user.company_id, payload.name, payload.website, payload.category
        )

        report = ResearchReport(
            competitor_id=competitor.id,
            name=competitor.name,
            category=competitor.category,
            website=competitor.website,
            founded_year=competitor.founded_year,
            pricing=pricing,
            features=features,
            insight=insight,
        )

        db.add(ResearchUsage(company_id=user.company_id, competitor_name=payload.name))
        db.add(ResearchHistory(
            company_id=user.company_id,
            user_id=user.id,
            competitor_id=competitor.id,
            competitor_name=competitor.name,
            website=competitor.website,
            category=competitor.category,
            result=report.model_dump(mode="json"),
        ))
        db.commit()
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception:
        logger.exception("Research call failed for %s", payload.name)
        raise HTTPException(status_code=502, detail="Research failed. Please try again.")

    return report