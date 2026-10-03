from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Subscription(Base):
    """The company's current paid plan state. One row per company, updated in place on renewal/upgrade."""

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    plan = Column(String(30), nullable=False, default="trial")
    provider = Column(String(20))  # "paypal" or "mpesa", null while on trial
    status = Column(String(20), nullable=False, default="trialing")  # trialing / active / past_due / cancelled

    paypal_subscription_id = Column(String(100))
    current_period_end = Column(DateTime)  # when the current paid period expires

    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    company = relationship("Company", backref="subscription", uselist=False)