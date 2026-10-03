from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class Payment(Base):
    """A log of every payment attempt from either provider, for support/auditing and renewal history."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)

    provider = Column(String(20), nullable=False)  # "paypal" or "mpesa"
    plan = Column(String(30), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)  # "USD" or "KES"
    status = Column(String(20), nullable=False, default="pending")

    provider_reference = Column(String(150))  # PayPal order/subscription ID, or M-Pesa CheckoutRequestID
    mpesa_receipt_number = Column(String(50))  

    created_at = Column(DateTime, nullable=False, default=utcnow)
    completed_at = Column(DateTime)

    company = relationship("Company")