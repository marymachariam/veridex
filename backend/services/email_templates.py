def verification_email(first_name: str, verify_url: str) -> tuple:
    """Returns (subject, title, body_html)."""
    subject = "Verify your VERIDEX account"
    title = "Confirm your email"
    body_html = f"""
        <p style="color: #475569; font-size: 15px;">Hi {first_name},</p>
        <p style="color: #475569; font-size: 15px;">
            Click below to verify your email and activate your VERIDEX account:
        </p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="{verify_url}" style="background-color: #2563EB; color: #FFFFFF; padding: 12px 28px;
               border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block;">
               Verify Email
            </a>
        </div>
        <p style="color: #94A3B8; font-size: 13px;">This link expires in 30 minutes.</p>
    """
    return subject, title, body_html


def password_reset_email(first_name: str, reset_url: str) -> tuple:
    subject = "Reset your VERIDEX password"
    title = "Password reset requested"
    body_html = f"""
        <p style="color: #475569; font-size: 15px;">Hi {first_name},</p>
        <p style="color: #475569; font-size: 15px;">
            Click below to set a new password. If you didn't request this, you can ignore this email.
        </p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="{reset_url}" style="background-color: #2563EB; color: #FFFFFF; padding: 12px 28px;
               border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block;">
               Reset Password
            </a>
        </div>
        <p style="color: #94A3B8; font-size: 13px;">This link expires in 30 minutes.</p>
    """
    return subject, title, body_html


def trial_started_email(first_name: str) -> tuple:
    subject = "Your VERIDEX 14-day trial has started"
    title = "Welcome to VERIDEX"
    body_html = f"""
        <p style="color: #475569; font-size: 15px;">Hi {first_name},</p>
        <p style="color: #475569; font-size: 15px;">
            Your free 14-day trial is now active. Start by researching your first competitor —
            VERIDEX will handle pricing, positioning, features, and SWOT automatically.
        </p>
    """
    return subject, title, body_html


def trial_ending_soon_email(first_name: str) -> tuple:
    subject = "Your VERIDEX trial ends tomorrow"
    title = "1 day left on your trial"
    body_html = f"""
        <p style="color: #475569; font-size: 15px;">Hi {first_name},</p>
        <p style="color: #475569; font-size: 15px;">
            Your VERIDEX trial ends tomorrow. Upgrade now to keep your research, alerts, and
            battlecards without interruption.
        </p>
    """
    return subject, title, body_html


def trial_ended_email(first_name: str) -> tuple:
    subject = "Your VERIDEX trial has ended"
    title = "Trial ended"
    body_html = f"""
        <p style="color: #475569; font-size: 15px;">Hi {first_name},</p>
        <p style="color: #475569; font-size: 15px;">
            Your 14-day trial has ended. Subscribe now to keep access to your competitor data,
            research, and alerts.
        </p>
    """
    return subject, title, body_html