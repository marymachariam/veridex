from fastapi import HTTPException, status
from typing import Optional


class Permission:
    """Permission levels for VERIDEX."""
    
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Role:
    """User roles for VERIDEX."""
    
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


def check_permission(user: dict, required_role: str) -> bool:
    """Check if user has required permission."""
    user_role = user.get("payload", {}).get("role", "viewer")
    
    role_hierarchy = {
        "admin": ["admin", "analyst", "viewer"],
        "analyst": ["analyst", "viewer"],
        "viewer": ["viewer"]
    }
    
    allowed_roles = role_hierarchy.get(user_role, ["viewer"])
    return required_role in allowed_roles


def require_admin(user: dict) -> dict:
    """Require admin role."""
    if not check_permission(user, "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


def require_analyst(user: dict) -> dict:
    """Require analyst role or higher."""
    if not check_permission(user, "analyst"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst access required"
        )
    return user


def require_authenticated(user: dict) -> dict:
    """Require any authenticated user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user


def has_data_access(user: dict, resource_id: int) -> bool:
    """Check if user has access to a specific resource."""
    user_role = user.get("payload", {}).get("role", "viewer")
    
    if user_role == "admin":
        return True
    
    user_resource_ids = user.get("payload", {}).get("accessible_resources", [])
    return resource_id in user_resource_ids