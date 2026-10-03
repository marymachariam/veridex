from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, true  
from sqlalchemy.orm import relationship

from core.clock import utcnow
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="viewer")
    is_active = Column(Boolean, nullable=False, default=True)
    onboarding_completed = Column(Boolean, nullable=False, default=False, server_default=true())
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    last_login_at = Column(DateTime)

    is_verified = Column(Boolean, nullable=False, default=False)
    google_id = Column(String(64), unique=True, index=True, nullable=True)

    company = relationship("Company", back_populates="users")
    