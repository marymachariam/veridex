from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.clock import utcnow
from core.config import settings
from core.constants import UserRole
from models.company import Company
from models.user import User
from schemas.auth_schema import UserRegister
from security.auth import hash_password


class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.get(User, user_id)

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.scalar(select(User).where(User.username == username.strip().lower()))

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.scalar(select(User).where(User.email == email.strip().lower()))

    @staticmethod
    def create_account(db: Session, data: UserRegister) -> User:
        """Every registration creates a NEW company and makes the user its admin.
        (Joining an existing company will be done through invitations, never by typing its name.)"""
        company = Company(
            name=data.company_name,
            industry=data.industry,
            plan="trial",
            subscription_status="trialing",
            trial_ends_at=utcnow() + timedelta(days=settings.TRIAL_DAYS),
        )
        db.add(company)
        db.flush()

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            role=UserRole.ADMIN.value,
            company_id=company.id,
        )
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(user)
        return user


user_repo = UserRepository()