from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.constants import UserRole
from database import get_db
from models.user import User
from repository.user_repo import user_repo
from security.auth import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

ROLE_RANK = {UserRole.VIEWER.value: 1, UserRole.ANALYST.value: 2, UserRole.ADMIN.value: 3}


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise unauthorized

    user = user_repo.get_by_id(db, user_id)
    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_role(minimum: UserRole):
    """viewer: read only. analyst: create and edit. admin: everything, including delete."""

    def checker(user: User = Depends(get_current_user)) -> User:
        if ROLE_RANK.get(user.role, 0) < ROLE_RANK[minimum.value]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{minimum.value} role required")
        return user

    return checker