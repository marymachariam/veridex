from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False



DUMMY_HASH = hash_password("not-a-real-password")


def create_access_token(subject: str, claims: Optional[dict] = None, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        **(claims or {}),
        "sub": subject,
        "iat": now,
        "exp": now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        options={"require": ["exp", "sub"]},
    )


def create_purpose_token(user_id: int, purpose: str, expires_minutes: int = 30) -> str:
    """A short-lived signed token for email verification or password reset links.
    Nothing is stored server-side - the signature and expiry are self-contained in the token."""
    return create_access_token(str(user_id), {"purpose": purpose}, timedelta(minutes=expires_minutes))


def decode_purpose_token(token: str, expected_purpose: str) -> int:
    """Returns the user_id if the token is valid, unexpired, and matches the expected purpose. Raises otherwise."""
    payload = decode_access_token(token)
    if payload.get("purpose") != expected_purpose:
        raise jwt.InvalidTokenError("Token purpose mismatch")
    return int(payload["sub"])