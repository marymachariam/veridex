from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, index=True)
    source = Column(String(50), nullable=False, default="Manual")
    rating = Column(Float)
    sentiment = Column(String(20), nullable=False, default="neutral")
    comment_summary = Column(Text)
    recorded_date = Column(DateTime, nullable=False, default=utcnow)

    competitor = relationship("Competitor", back_populates="reviews")