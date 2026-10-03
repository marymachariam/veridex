import logging

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from core.config import settings

logger = logging.getLogger("veridex.email")

BRAND_COLOR = "#2563EB"
BRAND_DARK = "#0F172A"


def _wrap_branded_html(title: str, body_html: str) -> str:
    """Wraps any email content in a consistent VERIDEX-branded shell."""
    return f"""
    <div style="font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif; max-width: 560px; margin: 0 auto; padding: 32px 24px;">
        <div style="text-align: center; margin-bottom: 24px;">
            <span style="font-size: 32px;">🏢</span>
            <h1 style="color: {BRAND_DARK}; font-size: 22px; font-weight: 800; margin: 8px 0 0 0;">VERIDEX</h1>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 28px;">
            <h2 style="color: {BRAND_DARK}; font-size: 18px; margin-top: 0;">{title}</h2>
            {body_html}
        </div>
        <p style="text-align: center; color: #94A3B8; font-size: 12px; margin-top: 24px;">
            VERIDEX — Automated Competitor Intelligence
        </p>
    </div>
    """


def send_email(to_email: str, to_name: str, subject: str, title: str, body_html: str) -> bool:
    """Sends a branded transactional email via Brevo. Returns True on success, False on failure (never raises)."""
    if not settings.BREVO_API_KEY:
        logger.warning("BREVO_API_KEY not configured - skipping email to %s", to_email)
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    full_html = _wrap_branded_html(title, body_html)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": settings.EMAIL_FROM_NAME, "email": settings.EMAIL_FROM_ADDRESS},
        to=[{"email": to_email, "name": to_name}],
        subject=subject,
        html_content=full_html,
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info("Email sent to %s: %s", to_email, subject)
        return True
    except ApiException as exc:
        print(f"!!! BREVO SEND FAILED for {to_email}: {exc}")
        logger.error("Brevo send failed for %s: %s", to_email, exc)
        return False
    except Exception as exc:
        print(f"!!! UNEXPECTED EMAIL ERROR for {to_email}: {exc}")
        logger.error("Unexpected email error for %s: %s", to_email, exc)
        return False