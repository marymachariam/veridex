from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class CompetitorInsight(Base):
    """One research report per competitor. Re-running research overwrites this row."""

    __tablename__ = "competitor_insights"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(
        Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )

    tagline = Column(String(300))
    target_market = Column(Text)
    summary = Column(Text)
    strengths = Column(Text)      # newline-separated bullet points
    weaknesses = Column(Text)
    opportunities = Column(Text)
    threats = Column(Text)
    recent_signals = Column(Text)  # funding, hiring, product launches, etc.

    sources = Column(Text)         # newline-separated URLs the model cited
    researched_at = Column(DateTime, nullable=False, default=utcnow)

    competitor = relationship("Competitor", backref="insight", uselist=False)