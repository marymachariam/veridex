from .theme import Colors, Icons
from .settings import settings, AppSettings

class Typography:
    pass

class Spacing:
    pass

class BillingPeriods:
    ALL = ["monthly", "annual", "one_time"]

class Sentiments:
    ALL = ["positive", "neutral", "negative"]

class ReviewSources:
    ALL = ["Trustpilot", "G2", "Capterra", "App Store", "Play Store"]

class Categories:
    ALL = ["CRM", "Project Management", "Communication", "Productivity"]

class ErrorMessages:
    GENERIC = "An error occurred"
    PRICING_NOT_FOUND = "Pricing not found"
    REVIEW_NOT_FOUND = "Review not found"
    PRICE_HISTORY_NOT_FOUND = "Price history not found"

class SuccessMessages:
    GENERIC = "Success"
    PRICING_CREATED = "Pricing tier added"
    PRICING_UPDATED = "Pricing tier updated"
    PRICING_DELETED = "Pricing tier deleted"
    REVIEW_CREATED = "Review added"
    REVIEW_UPDATED = "Review updated"
    REVIEW_DELETED = "Review deleted"
    PRICE_HISTORY_CREATED = "Price change logged"
    PRICE_HISTORY_UPDATED = "Price change updated"
    PRICE_HISTORY_DELETED = "Price change deleted"

class ValidationRules:
    PASS = True

__all__ = [
    "Colors", "Icons", "settings", "AppSettings", "Typography", "Spacing",
    "BillingPeriods", "Sentiments", "ReviewSources", "Categories",
    "ErrorMessages", "SuccessMessages", "ValidationRules"
]
