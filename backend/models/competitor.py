from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Competitor(Base):
    __tablename__ = "competitors"
    __table_args__ = (UniqueConstraint("company_id", "name", name="uq_competitor_company_name"),)

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    website = Column(String(255))
    founded_year = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    company = relationship("Company", back_populates="competitors")
    pricing = relationship("Pricing", back_populates="competitor", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="competitor", cascade="all, delete-orphan")
    features = relationship("Feature", back_populates="competitor", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="competitor", cascade="all, delete-orphan")