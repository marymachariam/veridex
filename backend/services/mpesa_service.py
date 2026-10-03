import base64
import logging
from datetime import datetime

import requests

from core.config import settings

logger = logging.getLogger("veridex.mpesa")


def _get_access_token() -> str:
    resp = requests.get(
        f"{settings.mpesa_base_url}/oauth/v1/generate?grant_type=client_credentials",
        auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _password_and_timestamp() -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp


def stk_push(phone_number: str, amount: int, account_reference: str, description: str) -> dict:
    """phone_number must be in format 2547XXXXXXXX (no +, no leading 0)."""
    token = _get_access_token()
    password, timestamp = _password_and_timestamp()

    resp = requests.post(
        f"{settings.mpesa_base_url}/mpesa/stkpush/v1/processrequest",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": account_reference[:20],
            "TransactionDesc": description[:20],
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def normalize_phone(raw: str) -> str:
    """Converts 07XXXXXXXX or +2547XXXXXXXX or 2547XXXXXXXX into the 2547XXXXXXXX format Daraja expects."""
    digits = "".join(ch for ch in raw if ch.isdigit())
    if digits.startswith("0"):
        return "254" + digits[1:]
    if digits.startswith("254"):
        return digits
    if digits.startswith("7") or digits.startswith("1"):
        return "254" + digits
    return digits