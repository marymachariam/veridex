"""
Application constants and enumerations
Used throughout the frontend for consistency
"""


class Categories:
    """Competitor categories"""
    
    CRM = "CRM"
    PROJECT_MANAGEMENT = "Project Management"
    PRODUCTIVITY = "Productivity"
    ANALYTICS = "Analytics"
    COMMUNICATION = "Communication"
    HUMAN_RESOURCES = "Human Resources"
    FINANCE = "Finance"
    MARKETING = "Marketing"
    SALES = "Sales"
    OTHER = "Other"
    
    ALL = [
        CRM,
        PROJECT_MANAGEMENT,
        PRODUCTIVITY,
        ANALYTICS,
        COMMUNICATION,
        HUMAN_RESOURCES,
        FINANCE,
        MARKETING,
        SALES,
        OTHER
    ]


class BillingPeriods:
    """Billing period options"""
    
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PER_USER_MONTH = "per user/month"
    PER_USER_YEAR = "per user/year"
    ONE_TIME = "one-time"
    CUSTOM = "custom"
    
    ALL = [
        MONTHLY,
        YEARLY,
        PER_USER_MONTH,
        PER_USER_YEAR,
        ONE_TIME,
        CUSTOM
    ]


class Sentiments:
    """Review sentiment types"""
    
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    
    ALL = [POSITIVE, NEUTRAL, NEGATIVE]
    
    EMOJI = {
        POSITIVE: "😊",
        NEUTRAL: "😐",
        NEGATIVE: "😞"
    }


class ReviewSources:
    """Sources for customer reviews"""
    
    G2 = "G2"
    CAPTERRA = "Capterra"
    REDDIT = "Reddit"
    TWITTER = "Twitter"
    TRUSTPILOT = "Trustpilot"
    PRODUCTHUNT = "ProductHunt"
    GARTNER = "Gartner"
    LINKEDIN = "LinkedIn"
    OTHER = "Other"
    
    ALL = [
        G2,
        CAPTERRA,
        REDDIT,
        TWITTER,
        TRUSTPILOT,
        PRODUCTHUNT,
        GARTNER,
        LINKEDIN,
        OTHER
    ]


class ValidationRules:
    """Input validation rules"""
    
    COMPETITOR_NAME_MIN = 1
    COMPETITOR_NAME_MAX = 255
    
    TIER_NAME_MIN = 1
    TIER_NAME_MAX = 100
    
    FEATURE_NAME_MIN = 1
    FEATURE_NAME_MAX = 255
    
    DESCRIPTION_MAX = 1000
    COMMENT_MAX = 1000
    
    PRICE_MIN = 0
    PRICE_MAX = 999999.99
    
    RATING_MIN = 0
    RATING_MAX = 5
    
    FOUNDED_YEAR_MIN = 1900
    FOUNDED_YEAR_MAX = 2025


class ErrorMessages:
    """Error messages shown to users"""
    
    # Generic Errors
    GENERIC_ERROR = "An error occurred. Please try again."
    CONNECTION_ERROR = "Failed to connect to server. Check your internet connection."
    TIMEOUT_ERROR = "Request timed out. Please try again."
    
    # Validation Errors
    COMPETITOR_NAME_REQUIRED = "Competitor name is required"
    COMPETITOR_NAME_EXISTS = "A competitor with this name already exists"
    CATEGORY_REQUIRED = "Category is required"
    
    TIER_NAME_REQUIRED = "Tier name is required"
    PRICE_INVALID = "Price must be a positive number"
    BILLING_PERIOD_REQUIRED = "Billing period is required"
    
    RATING_INVALID = "Rating must be between 0 and 5"
    SENTIMENT_REQUIRED = "Sentiment type is required"
    SOURCE_REQUIRED = "Review source is required"
    
    FEATURE_NAME_REQUIRED = "Feature name is required"
    
    # Database Errors
    COMPETITOR_NOT_FOUND = "Competitor not found"
    PRICING_NOT_FOUND = "Pricing tier not found"
    REVIEW_NOT_FOUND = "Review not found"
    FEATURE_NOT_FOUND = "Feature not found"
    PRICE_HISTORY_NOT_FOUND = "Price history record not found"
    
    # Permission Errors
    ACCESS_DENIED = "You don't have permission to access this resource"
    AUTHENTICATION_REQUIRED = "Please log in to continue"
    
    # API Errors
    API_400 = "Invalid request. Please check your input."
    API_401 = "Authentication failed. Please log in again."
    API_403 = "Access forbidden."
    API_404 = "Resource not found."
    API_500 = "Server error. Please try again later."


class SuccessMessages:
    """Success messages shown to users"""
    
    COMPETITOR_CREATED = "Competitor added successfully"
    COMPETITOR_UPDATED = "Competitor updated successfully"
    COMPETITOR_DELETED = "Competitor deleted successfully"
    
    PRICING_CREATED = "Pricing tier added successfully"
    PRICING_UPDATED = "Pricing tier updated successfully"
    PRICING_DELETED = "Pricing tier deleted successfully"
    
    REVIEW_CREATED = "Review added successfully"
    REVIEW_UPDATED = "Review updated successfully"
    REVIEW_DELETED = "Review deleted successfully"
    
    FEATURE_CREATED = "Feature added successfully"
    FEATURE_UPDATED = "Feature updated successfully"
    FEATURE_DELETED = "Feature deleted successfully"
    
    PRICE_HISTORY_CREATED = "Price change logged successfully"
    PRICE_HISTORY_UPDATED = "Price history updated successfully"
    PRICE_HISTORY_DELETED = "Price history deleted successfully"
    
    DATA_EXPORTED = "Data exported successfully"
    DATA_IMPORTED = "Data imported successfully"


class WarningMessages:
    """Warning messages shown to users"""
    
    DELETE_CONFIRMATION = "Are you sure? This action cannot be undone."
    UNSAVED_CHANGES = "You have unsaved changes. Leave without saving?"
    DUPLICATE_ENTRY = "This entry might be a duplicate. Continue anyway?"


class InfoMessages:
    """Informational messages"""
    
    NO_DATA = "No data available. Add data to get started."
    LOADING = "Loading..."
    SEARCHING = "Searching..."
    EMPTY_RESULTS = "No results found. Try adjusting your filters."
    
    AVERAGE_PRICE = "Average price across all tiers"
    PRICE_INCREASE = "Price increase since last change"
    CUSTOMER_SATISFACTION = "Based on customer reviews"
    MOST_COMMON_FEATURE = "Most frequently mentioned feature"


class DateRangePresets:
    """Date range filter presets"""
    
    LAST_7_DAYS = "Last 7 Days"
    LAST_30_DAYS = "Last 30 Days"
    LAST_90_DAYS = "Last 90 Days"
    LAST_YEAR = "Last Year"
    ALL_TIME = "All Time"
    CUSTOM = "Custom Date Range"


class SortOptions:
    """Sorting options for tables"""
    
    ASCENDING = "ascending"
    DESCENDING = "descending"
    
    BY_NAME = "Name"
    BY_PRICE = "Price"
    BY_RATING = "Rating"
    BY_DATE = "Date Added"
    BY_RECENT = "Most Recent"


class PageLimits:
    """Pagination limits"""
    
    ROWS_10 = 10
    ROWS_20 = 20
    ROWS_50 = 50
    ROWS_100 = 100
    
    ALL_OPTIONS = [10, 20, 50, 100]


class ChartTypes:
    """Available chart types"""
    
    BAR = "bar"
    LINE = "line"
    AREA = "area"
    SCATTER = "scatter"
    PIE = "pie"
    DONUT = "donut"
    GAUGE = "gauge"


class MetricUnits:
    """Units for displaying metrics"""
    
    PRICE = "USD"
    PERCENTAGE = "%"
    RATING = "/ 5"
    COUNT = "items"
    INCREASE = "increase"
    DECREASE = "decrease"


class APIEndpoints:
    """API endpoint paths (relative to base URL)"""
    
    # Health & Status
    HEALTH = "/health"
    
    # Competitors
    COMPETITORS = "/api/v1/competitors"
    COMPETITORS_BY_ID = "/api/v1/competitors/{id}"
    COMPETITORS_BY_CATEGORY = "/api/v1/competitors/category/{category}"
    
    # Pricing
    PRICING = "/api/v1/pricing"
    PRICING_BY_ID = "/api/v1/pricing/{id}"
    PRICING_BY_COMPETITOR = "/api/v1/pricing/competitor/{competitor_id}"
    
    # Reviews
    REVIEWS = "/api/v1/reviews"
    REVIEWS_BY_ID = "/api/v1/reviews/{id}"
    REVIEWS_BY_COMPETITOR = "/api/v1/reviews/competitor/{competitor_id}"
    REVIEWS_AVERAGE_RATING = "/api/v1/reviews/competitor/{competitor_id}/average-rating"
    REVIEWS_SENTIMENT = "/api/v1/reviews/competitor/{competitor_id}/sentiment-distribution"
    
    # Features
    FEATURES = "/api/v1/features"
    FEATURES_BY_ID = "/api/v1/features/{id}"
    FEATURES_BY_COMPETITOR = "/api/v1/features/competitor/{competitor_id}"
    FEATURES_BY_TIER = "/api/v1/features/competitor/{competitor_id}/tier/{tier}"
    FEATURES_COUNT = "/api/v1/features/competitor/{competitor_id}/count"
    
    # Price History
    PRICE_HISTORY = "/api/v1/price-history"
    PRICE_HISTORY_BY_ID = "/api/v1/price-history/{id}"
    PRICE_HISTORY_BY_COMPETITOR = "/api/v1/price-history/competitor/{competitor_id}"
    PRICE_HISTORY_BY_TIER = "/api/v1/price-history/competitor/{competitor_id}/tier/{tier_name}"
    PRICE_HISTORY_AVERAGE = "/api/v1/price-history/competitor/{competitor_id}/average-increase"


class CacheKeys:
    """Cache key naming convention"""
    
    COMPETITORS = "competitors"
    COMPETITORS_BY_CATEGORY = "competitors_category_{category}"
    PRICING = "pricing"
    PRICING_BY_COMPETITOR = "pricing_competitor_{id}"
    REVIEWS = "reviews"
    REVIEWS_BY_COMPETITOR = "reviews_competitor_{id}"
    FEATURES = "features"
    FEATURES_BY_COMPETITOR = "features_competitor_{id}"
    PRICE_HISTORY = "price_history"
    PRICE_HISTORY_BY_COMPETITOR = "price_history_competitor_{id}"


class Icons:
    """Icon/emoji mappings for visual consistency"""
    
    COMPETITOR = "🏢"
    PRICING = "💰"
    FEATURES = "⚙️"
    REVIEWS = "💬"
    SENTIMENT_POSITIVE = "😊"
    SENTIMENT_NEUTRAL = "😐"
    SENTIMENT_NEGATIVE = "😞"
    TRENDING_UP = "📈"
    TRENDING_DOWN = "📉"
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠️"
    INFO = "ℹ️"
    SEARCH = "🔍"
    FILTER = "🔗"
    EXPORT = "📥"
    IMPORT = "📤"
    DELETE = "🗑️"
    EDIT = "✏️"
    ADD = "+"
    CLOSE = "✕"
    REFRESH = "🔄"


# Export all constants for easy importing
CONSTANTS = {
    "categories": Categories,
    "billing_periods": BillingPeriods,
    "sentiments": Sentiments,
    "sources": ReviewSources,
    "validation": ValidationRules,
    "errors": ErrorMessages,
    "success": SuccessMessages,
    "warnings": WarningMessages,
    "info": InfoMessages,
    "endpoints": APIEndpoints,
    "cache_keys": CacheKeys,
    "icons": Icons
}