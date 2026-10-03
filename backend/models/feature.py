from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name = Column(String(255), nullable=False)
    tier_available = Column(String(100))
    recorded_date = Column(DateTime, nullable=False, default=utcnow)

    competitor = relationship("Competitor", back_populates="features")