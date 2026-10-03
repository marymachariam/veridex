import logging
import re
import secrets
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, URLSafeTimedSerializer
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.clock import utcnow
from core.config import settings
from database import get_db
from models.user import User
from repository.user_repo import user_repo
from schemas.auth_schema import Token, UserLogin, UserRead, UserRegister
from security.auth import (
    DUMMY_HASH,
    create_access_token,
    create_purpose_token,
    decode_purpose_token,
    hash_password,
    verify_password,
)
from security.deps import get_current_user
from services.email_service import send_email
from services.email_templates import password_reset_email, trial_started_email, verification_email

logger = logging.getLogger("veridex.auth")
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

FRONTEND_URL = settings.FRONTEND_URL or "http://localhost:8501"


class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class GoogleExchangeRequest(BaseModel):
    code: str


@router.post("/register", response_model=UserRead)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if user_repo.get_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if user_repo.get_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        user = user_repo.create_account(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    token = create_purpose_token(user.id, "verify_email")
    verify_url = f"{FRONTEND_URL}/Verify_Email?token={token}"
    subject, title, body = verification_email(user.first_name, verify_url)
    if not send_email(user.email, user.first_name, subject, title, body):
        logger.warning("Could not send verification email to %s", user.email)

    return user


@router.post("/verify-email", response_model=Token)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    try:
        user_id = decode_purpose_token(payload.token, "verify_email")
    except Exception:
        raise HTTPException(status_code=400, detail="This verification link is invalid or has expired.")

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="This email is already verified")

    user.is_verified = True
    user.last_login_at = utcnow()
    db.commit()

    subject, title, body = trial_started_email(user.first_name)
    send_email(user.email, user.first_name, subject, title, body)

    token = create_access_token(str(user.id), {"cid": user.company_id, "role": user.role})
    return Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@router.post("/resend-verification")
def resend_verification(payload: ResendVerificationRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, payload.email.strip().lower())
    if user is None or user.is_verified:
        return {"message": "If that email exists and is unverified, a new link has been sent."}

    token = create_purpose_token(user.id, "verify_email")
    verify_url = f"{FRONTEND_URL}/Verify_Email?token={token}"
    subject, title, body = verification_email(user.first_name, verify_url)
    send_email(user.email, user.first_name, subject, title, body)
    return {"message": "If that email exists and is unverified, a new link has been sent."}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, payload.email.strip().lower())
    if user is not None:
        token = create_purpose_token(user.id, "reset_password")
        reset_url = f"{FRONTEND_URL}/Reset_Password?token={token}"
        subject, title, body = password_reset_email(user.first_name, reset_url)
        send_email(user.email, user.first_name, subject, title, body)
    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        user_id = decode_purpose_token(payload.token, "reset_password")
    except Exception:
        raise HTTPException(status_code=400, detail="This reset link is invalid or has expired.")

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if len(payload.new_password.encode("utf-8")) > 72 or len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be 8-72 characters.")

    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password reset successfully. You can now log in."}


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    identifier = payload.username.strip().lower()
    user = user_repo.get_by_email(db, identifier) if "@" in identifier else user_repo.get_by_username(db, identifier)

    if user is None:
        verify_password(payload.password, DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in.")

    user.last_login_at = utcnow()
    db.commit()

    token = create_access_token(str(user.id), {"cid": user.company_id, "role": user.role})
    return Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/onboarding/complete")
def complete_onboarding(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.get(User, user.id)
    db_user.onboarding_completed = True
    db.commit()
    return {"onboarding_completed": True}


# ---------------------------------------------------------------------------
# Google sign-in
# ---------------------------------------------------------------------------

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

_state_signer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="google-oauth-state")


def _google_fail(message: str, reason: str = "") -> RedirectResponse:
    logger.warning("Google sign-in failed: %s %s", message, reason)
    return RedirectResponse(f"{FRONTEND_URL}/Login?{urlencode({'google_error': message})}")


@router.get("/google/login")
def google_login():
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Google sign-in is not configured")
    state = _state_signer.dumps({"n": secrets.token_urlsafe(8)})
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/google/callback")
def google_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    if error or not code or not state:
        return _google_fail("Google sign-in was cancelled.", f"error={error}")

    try:
        _state_signer.loads(state, max_age=600)
    except BadSignature:
        return _google_fail("Sign-in session expired. Please try again.", "bad or expired state")

    try:
        tok = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            timeout=15,
        )
        tok.raise_for_status()
        info = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {tok.json()['access_token']}"},
            timeout=15,
        )
        info.raise_for_status()
        info = info.json()
    except (requests.RequestException, KeyError, ValueError):
        logger.exception("Google token exchange failed")
        return _google_fail("Could not complete Google sign-in. Please try again.")

    email = (info.get("email") or "").strip().lower()
    if not email or not info.get("email_verified"):
        return _google_fail("Your Google email is not verified.", f"email={email!r}")

    user = user_repo.get_by_email(db, email)
    is_new = False

    if user is None:
        first = (info.get("given_name") or email.split("@")[0]).strip()[:100] or "User"
        last = (info.get("family_name") or "-").strip()[:100] or "-"
        base = re.sub(r"[^a-z0-9_.-]", "", email.split("@")[0])[:40] or "user"
        username = base
        while len(username) < 3 or user_repo.get_by_username(db, username):
            username = f"{base}{secrets.randbelow(10000)}"

        payload = UserRegister(
            email=email,
            username=username,
            password=secrets.token_urlsafe(32), 
            first_name=first,
            last_name=last,
            company_name=f"{first}'s Company",
            industry="Other",
        )
        try:
            user = user_repo.create_account(db, payload)
        except IntegrityError:
            db.rollback()
            return _google_fail("Could not create your account. Please try again.", "integrity error")
        is_new = True

    if not user.is_active:
        return _google_fail("This account is disabled.")

    user.is_verified = True  
    user.last_login_at = utcnow()
    db.commit()

    if is_new:
        subject, title, body = trial_started_email(user.first_name)
        send_email(user.email, user.first_name, subject, title, body)

    login_code = create_purpose_token(user.id, "google_login")
    return RedirectResponse(f"{FRONTEND_URL}/Login?{urlencode({'google_code': login_code})}")


@router.post("/google/exchange", response_model=Token)
def google_exchange(payload: GoogleExchangeRequest, db: Session = Depends(get_db)):
    try:
        user_id = decode_purpose_token(payload.code, "google_login")
    except Exception:
        raise HTTPException(status_code=400, detail="Google sign-in link is invalid or has expired.")
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id), {"cid": user.company_id, "role": user.role})
    return Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)