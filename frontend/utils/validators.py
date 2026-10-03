"""
Input validation utilities for form data
Ensures data integrity before sending to backend
"""

import re
from typing import Optional, Tuple, Any, List
import logging

from config import ValidationRules, ErrorMessages

logger = logging.getLogger(__name__)


class Validator:
    """Professional input validation for VERIDEX frontend"""
    
    # ========================================================================
    # COMPETITOR VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_competitor_name(name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate competitor name
        
        Args:
            name: Competitor name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, ErrorMessages.COMPETITOR_NAME_REQUIRED
        
        name = name.strip()
        
        if len(name) < ValidationRules.COMPETITOR_NAME_MIN:
            return False, f"Name must be at least {ValidationRules.COMPETITOR_NAME_MIN} character"
        
        if len(name) > ValidationRules.COMPETITOR_NAME_MAX:
            return False, f"Name must not exceed {ValidationRules.COMPETITOR_NAME_MAX} characters"
        
        # Check for invalid characters
        if not re.match(r"^[a-zA-Z0-9\s\-\.&()]+$", name):
            return False, "Name contains invalid characters"
        
        return True, None
    
    @staticmethod
    def validate_category(category: str) -> Tuple[bool, Optional[str]]:
        """
        Validate category
        
        Args:
            category: Category name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not category or not category.strip():
            return False, ErrorMessages.CATEGORY_REQUIRED
        
        return True, None
    
    @staticmethod
    def validate_website(website: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate website URL
        
        Args:
            website: Website URL
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not website or website.strip() == "":
            return True, None  # Optional field
        
        website = website.strip()
        
        # Simple URL validation
        url_pattern = r"^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}.*$"
        
        if not re.match(url_pattern, website):
            return False, "Invalid website URL format"
        
        return True, None
    
    @staticmethod
    def validate_founded_year(year: Optional[int]) -> Tuple[bool, Optional[str]]:
        """
        Validate founded year
        
        Args:
            year: Founded year
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if year is None:
            return True, None  # Optional field
        
        if year < ValidationRules.FOUNDED_YEAR_MIN or year > ValidationRules.FOUNDED_YEAR_MAX:
            return False, f"Year must be between {ValidationRules.FOUNDED_YEAR_MIN} and {ValidationRules.FOUNDED_YEAR_MAX}"
        
        return True, None
    
    # ========================================================================
    # PRICING VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_tier_name(tier_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate pricing tier name
        
        Args:
            tier_name: Tier name (Pro, Enterprise, etc.)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not tier_name or not tier_name.strip():
            return False, ErrorMessages.TIER_NAME_REQUIRED
        
        tier_name = tier_name.strip()
        
        if len(tier_name) < ValidationRules.TIER_NAME_MIN:
            return False, f"Tier name must be at least {ValidationRules.TIER_NAME_MIN} character"
        
        if len(tier_name) > ValidationRules.TIER_NAME_MAX:
            return False, f"Tier name must not exceed {ValidationRules.TIER_NAME_MAX} characters"
        
        return True, None
    
    @staticmethod
    def validate_price(price: Optional[float]) -> Tuple[bool, Optional[str]]:
        """
        Validate pricing amount
        
        Args:
            price: Price in USD
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if price is None or price == "":
            return True, None  # Optional field
        
        try:
            price_float = float(price)
            
            if price_float < ValidationRules.PRICE_MIN:
                return False, f"Price must be at least {ValidationRules.PRICE_MIN}"
            
            if price_float > ValidationRules.PRICE_MAX:
                return False, f"Price must not exceed {ValidationRules.PRICE_MAX}"
            
            return True, None
        except (ValueError, TypeError):
            return False, ErrorMessages.PRICE_INVALID
    
    @staticmethod
    def validate_billing_period(period: str) -> Tuple[bool, Optional[str]]:
        """
        Validate billing period
        
        Args:
            period: Billing period (monthly, yearly, etc.)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not period or not period.strip():
            return False, ErrorMessages.BILLING_PERIOD_REQUIRED
        
        valid_periods = [
            "monthly",
            "yearly",
            "per user/month",
            "per user/year",
            "one-time",
            "custom"
        ]
        
        if period.lower() not in valid_periods:
            return False, f"Invalid billing period"
        
        return True, None
    
    @staticmethod
    def validate_description(description: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate description text
        
        Args:
            description: Description text
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not description or description.strip() == "":
            return True, None  # Optional field
        
        if len(description) > ValidationRules.DESCRIPTION_MAX:
            return False, f"Description must not exceed {ValidationRules.DESCRIPTION_MAX} characters"
        
        return True, None
    
    # ========================================================================
    # REVIEW VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_rating(rating: Optional[float]) -> Tuple[bool, Optional[str]]:
        """
        Validate customer rating
        
        Args:
            rating: Rating value (0-5)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if rating is None or rating == "":
            return True, None  # Optional field
        
        try:
            rating_float = float(rating)
            
            if rating_float < ValidationRules.RATING_MIN or rating_float > ValidationRules.RATING_MAX:
                return False, f"Rating must be between {ValidationRules.RATING_MIN} and {ValidationRules.RATING_MAX}"
            
            return True, None
        except (ValueError, TypeError):
            return False, ErrorMessages.RATING_INVALID
    
    @staticmethod
    def validate_sentiment(sentiment: str) -> Tuple[bool, Optional[str]]:
        """
        Validate sentiment type
        
        Args:
            sentiment: Sentiment (positive, neutral, negative)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not sentiment or not sentiment.strip():
            return False, ErrorMessages.SENTIMENT_REQUIRED
        
        valid_sentiments = ["positive", "neutral", "negative"]
        
        if sentiment.lower() not in valid_sentiments:
            return False, "Sentiment must be positive, neutral, or negative"
        
        return True, None
    
    @staticmethod
    def validate_review_source(source: str) -> Tuple[bool, Optional[str]]:
        """
        Validate review source
        
        Args:
            source: Review source (G2, Capterra, etc.)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not source or not source.strip():
            return False, ErrorMessages.SOURCE_REQUIRED
        
        valid_sources = [
            "G2",
            "Capterra",
            "Reddit",
            "Twitter",
            "Trustpilot",
            "ProductHunt",
            "Gartner",
            "LinkedIn",
            "Other"
        ]
        
        if source not in valid_sources:
            return False, f"Invalid review source"
        
        return True, None
    
    @staticmethod
    def validate_comment(comment: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate review comment
        
        Args:
            comment: Comment text
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not comment or comment.strip() == "":
            return True, None  # Optional field
        
        if len(comment) > ValidationRules.COMMENT_MAX:
            return False, f"Comment must not exceed {ValidationRules.COMMENT_MAX} characters"
        
        return True, None
    
    # ========================================================================
    # FEATURE VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_feature_name(feature_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate feature name
        
        Args:
            feature_name: Feature name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not feature_name or not feature_name.strip():
            return False, ErrorMessages.FEATURE_NAME_REQUIRED
        
        feature_name = feature_name.strip()
        
        if len(feature_name) < ValidationRules.FEATURE_NAME_MIN:
            return False, f"Feature name must be at least {ValidationRules.FEATURE_NAME_MIN} character"
        
        if len(feature_name) > ValidationRules.FEATURE_NAME_MAX:
            return False, f"Feature name must not exceed {ValidationRules.FEATURE_NAME_MAX} characters"
        
        return True, None
    
    # ========================================================================
    # PRICE HISTORY VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_price_change(old_price: Optional[float], new_price: Optional[float]) -> Tuple[bool, Optional[str]]:
        """
        Validate price change (old and new prices)
        
        Args:
            old_price: Old price
            new_price: New price
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate old price
        valid_old, error_old = Validator.validate_price(old_price)
        if not valid_old:
            return False, error_old
        
        # Validate new price
        valid_new, error_new = Validator.validate_price(new_price)
        if not valid_new:
            return False, error_new
        
        return True, None
    
    # ========================================================================
    # GENERAL VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_required_field(value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a field is not empty
        
        Args:
            value: Field value
            field_name: Field name for error message
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, f"{field_name} is required"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email address
        
        Args:
            email: Email address
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email is required"
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
        if not re.match(email_pattern, email):
            return False, "Invalid email address"
        
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength
        
        Args:
            password: Password
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain lowercase letters"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain uppercase letters"
        
        if not re.search(r"[0-9]", password):
            return False, "Password must contain numbers"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain special characters"
        
        return True, None
    
    # ========================================================================
    # BATCH VALIDATION
    # ========================================================================
    
    @staticmethod
    def validate_competitor_form(form_data: dict) -> Tuple[bool, List[str]]:
        """
        Validate entire competitor form
        
        Args:
            form_data: Form data dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate name
        valid, error = Validator.validate_competitor_name(form_data.get("name", ""))
        if not valid:
            errors.append(error)
        
        # Validate category
        valid, error = Validator.validate_category(form_data.get("category", ""))
        if not valid:
            errors.append(error)
        
        # Validate website (optional)
        if form_data.get("website"):
            valid, error = Validator.validate_website(form_data.get("website"))
            if not valid:
                errors.append(error)
        
        # Validate founded year (optional)
        if form_data.get("founded_year"):
            valid, error = Validator.validate_founded_year(form_data.get("founded_year"))
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_pricing_form(form_data: dict) -> Tuple[bool, List[str]]:
        """
        Validate entire pricing form
        
        Args:
            form_data: Form data dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate tier name
        valid, error = Validator.validate_tier_name(form_data.get("tier_name", ""))
        if not valid:
            errors.append(error)
        
        # Validate price (optional)
        if form_data.get("price_usd") is not None:
            valid, error = Validator.validate_price(form_data.get("price_usd"))
            if not valid:
                errors.append(error)
        
        # Validate billing period
        valid, error = Validator.validate_billing_period(form_data.get("billing_period", ""))
        if not valid:
            errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_review_form(form_data: dict) -> Tuple[bool, List[str]]:
        """
        Validate entire review form
        
        Args:
            form_data: Form data dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate source
        valid, error = Validator.validate_review_source(form_data.get("source", ""))
        if not valid:
            errors.append(error)
        
        # Validate sentiment
        valid, error = Validator.validate_sentiment(form_data.get("sentiment", ""))
        if not valid:
            errors.append(error)
        
        # Validate rating (optional)
        if form_data.get("rating") is not None:
            valid, error = Validator.validate_rating(form_data.get("rating"))
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors


# Global validator instance
validator = Validator()