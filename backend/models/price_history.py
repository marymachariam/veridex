from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False, index=True)
    tier_name = Column(String(100), nullable=False)
    old_price = Column(Float)
    new_price = Column(Float)
    change_date = Column(DateTime, nullable=False, default=utcnow)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    competitor = relationship("Competitor", back_populates="price_history")

    @property
    def change_percent(self):
        if not self.old_price or self.new_price is None:
            return None
        return round((self.new_price - self.old_price) / self.old_price * 100, 2)