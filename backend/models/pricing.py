from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Pricing(Base):
    __tablename__ = "pricing"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, index=True)
    tier_name = Column(String(100), nullable=False)
    price_usd = Column(Float)  
    billing_period = Column(String(20), nullable=False, default="monthly")
    description = Column(Text)
    recorded_date = Column(DateTime, nullable=False, default=utcnow)

    competitor = relationship("Competitor", back_populates="pricing")