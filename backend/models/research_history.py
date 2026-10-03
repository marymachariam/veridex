from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, Integer, String

from core.clock import utcnow
from database import Base


class ResearchHistory(Base):
    __tablename__ = "research_history"
    __table_args__ = (Index("ix_research_history_company_created", "company_id", "created_at"),)

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="SET NULL"), nullable=True, index=True)
    competitor_name = Column(String(200), nullable=False, index=True)
    website = Column(String(255))
    category = Column(String(100))
    result = Column(JSON, nullable=False)  
    created_at = Column(DateTime, nullable=False, default=utcnow, index=True)