from enum import Enum

class CompetitorCategory(str, Enum):
    CRM = "CRM"
    PROJECT_MANAGEMENT = "Project Management"
    COMMUNICATION = "Communication"
    PRODUCTIVITY = "Productivity"

class BillingPeriod(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"
    ONE_TIME = "one_time"

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class ReviewSource(str, Enum):
    TRUSTPILOT = "Trustpilot"
    G2 = "G2"
    CAPTERRA = "Capterra"
    APPSTORE = "App Store"
    PLAYSTORE = "Play Store"

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class PlanTier(str, Enum):
    TRIAL = "trial"
    STARTER = "starter"
    PRO = "pro"


PLAN_PRICES_USD = {
    PlanTier.STARTER.value: 19.00,
    PlanTier.PRO.value: 49.00,
}

PLAN_PRICES_KES = {
    PlanTier.STARTER.value: 2500.00,
    PlanTier.PRO.value: 6500.00,
}

PLAN_LIMITS = {
    PlanTier.TRIAL.value: {"max_competitors": 3, "max_research_runs": 5},
    PlanTier.STARTER.value: {"max_competitors": 10, "max_research_runs": 50},
    PlanTier.PRO.value: {"max_competitors": None, "max_research_runs": None},
}


class PaymentProvider(str, Enum):
    PAYPAL = "paypal"
    MPESA = "mpesa"
    
PAYPAL_PLAN_IDS = {
    "starter": "P-0EV86851H2868743UNK6GV7Y",
    "pro": "P-6W3235281D4709036NK6GWAQ",
}

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"