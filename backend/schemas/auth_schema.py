from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=64)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    company_name: str = Field(min_length=2, max_length=200)
    industry: str = Field(default="Other", max_length=100)

    @field_validator("email", "username")
    @classmethod
    def _lowercase(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def _bcrypt_limit(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        return v

    @field_validator("first_name", "last_name", "company_name")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("This field cannot be empty")
        return v


class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=255)  # username or email
    password: str = Field(min_length=1, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    industry: Optional[str] = None
    plan: str
    subscription_status: str
    trial_ends_at: Optional[datetime] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    company: CompanyRead   
    onboarding_completed: bool = True
    