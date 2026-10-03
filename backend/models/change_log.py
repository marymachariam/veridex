from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class ChangeLog(Base):
    """One row per detected change, created when research is re-run and something differs from last time."""

    __tablename__ = "change_log"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, index=True)

    change_type = Column(String(30), nullable=False)  # "pricing", "feature_added", "feature_removed", "positioning"
    summary = Column(Text, nullable=False)              # human-readable: "Pro tier changed from $49 to $39"
    old_value = Column(Text)
    new_value = Column(Text)

    detected_at = Column(DateTime, nullable=False, default=utcnow)
    is_read = Column(Integer, nullable=False, default=0)  # 0/1 instead of Boolean for simple SQLite/Postgres parity

    competitor = relationship("Competitor")