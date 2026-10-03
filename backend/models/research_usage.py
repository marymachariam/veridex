from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from core.clock import utcnow
from database import Base


class ResearchUsage(Base):
    """One row per research run, used to enforce plan quotas. Never deleted - acts as an audit log too."""

    __tablename__ = "research_usage"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)