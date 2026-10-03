from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_TITLE: str = "VERIDEX"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Competitor and market intelligence platform"

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = "sqlite:///./veridex.db"
    DATABASE_ECHO: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    TRIAL_DAYS: int = 14
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000"]
    FRONTEND_URL: str = "http://localhost:8501"

    # Research agent
    GROQ_API_KEY: str = ""
    GROQ_API_KEYS: str = ""
    GEMINI_API_KEYS: str = ""
    TAVILY_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Chatbot (separate Groq key)
    GROQ_BOT_API_KEY: str = ""
    GROQ_BOT_MODEL: str = "openai/gpt-oss-120b"

    # Google login
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # PayPal
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_MODE: str = "sandbox"
    PAYPAL_WEBHOOK_ID: str = ""

    # M-Pesa (Daraja)
    MPESA_CONSUMER_KEY: str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_SHORTCODE: str = ""
    MPESA_PASSKEY: str = ""
    MPESA_ENV: str = "sandbox"
    MPESA_CALLBACK_URL: str = ""
    MPESA_CALLBACK_SECRET: str = ""

    # Email
    BREVO_API_KEY: str = ""
    EMAIL_FROM_ADDRESS: str = "maryymachariam@gmail.com"
    EMAIL_FROM_NAME: str = "VERIDEX"

    @property
    def paypal_base_url(self) -> str:
        return "https://api-m.sandbox.paypal.com" if self.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

    @property
    def mpesa_base_url(self) -> str:
        return "https://sandbox.safaricom.co.ke" if self.MPESA_ENV == "sandbox" else "https://api.safaricom.co.ke"

    @property
    def groq_api_key_list(self) -> list:
        return [k.strip() for k in self.GROQ_API_KEYS.split(",") if k.strip()]

    @property
    def gemini_api_key_list(self) -> list:
        return [k.strip() for k in self.GEMINI_API_KEYS.split(",") if k.strip()]

    @field_validator("SECRET_KEY")
    @classmethod
    def _secret_is_strong(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters. Generate one with: "
                'python -c "import secrets; print(secrets.token_urlsafe(48))"'
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def _normalize_db_url(cls, v: str) -> str:
        for prefix in ("postgres://", "postgresql://"):
            if v.startswith(prefix):
                return "postgresql+psycopg2://" + v[len(prefix):]
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


settings = Settings()