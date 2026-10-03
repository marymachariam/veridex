from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    industry = Column(String(100))
    website = Column(String(255))

    plan = Column(String(30), nullable=False, default="trial")
    subscription_status = Column(String(30), nullable=False, default="trialing")
    trial_ends_at = Column(DateTime)

    created_at = Column(DateTime, nullable=False, default=utcnow)

    users = relationship("User", back_populates="company")
    competitors = relationship("Competitor", back_populates="company", cascade="all, delete-orphan")