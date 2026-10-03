import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from database import SessionLocal
from models.competitor import Competitor
from routers.research_router import _run_research_and_diff  # reuse the same logic as the manual endpoint

logger = logging.getLogger("veridex.scheduler")

scheduler = BackgroundScheduler()


def run_scheduled_research():
    """Re-researches every tracked competitor across all companies. Runs on a schedule, not per-request."""
    db = SessionLocal()
    try:
        competitors = db.scalars(select(Competitor)).all()
        logger.info("Scheduled research starting for %d competitors", len(competitors))

        for competitor in competitors:
            try:
                _run_research_and_diff(db, competitor.company_id, competitor.name, competitor.website, competitor.category)
                logger.info("Scheduled research completed for competitor_id=%s (%s)", competitor.id, competitor.name)
            except Exception:
                logger.exception("Scheduled research FAILED for competitor_id=%s (%s)", competitor.id, competitor.name)
    finally:
        db.close()


def start_scheduler():
    # Runs once every 24 hours. Change to hours=168 for weekly if you'd rather not burn API credits daily.
    scheduler.add_job(run_scheduled_research, "interval", hours=24, id="research_refresh", replace_existing=True)
    scheduler.start()
    logger.info("Background scheduler started: research refresh every 24 hours")