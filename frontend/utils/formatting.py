"""
Data formatting utilities for displaying information in UI
Ensures consistent formatting across the entire application
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Union, Any
import logging

from config import (
    settings,
    Colors,
    Icons,
    Sentiments,
    MetricUnits
)

logger = logging.getLogger(__name__)


class Formatter:
    """Professional data formatting for VERIDEX frontend"""
    
    # ========================================================================
    # CURRENCY FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_price(price: Optional[Union[float, Decimal]]) -> str:
        """
        Format price as currency string
        
        Args:
            price: Price value
            
        Returns:
            Formatted price string (e.g., "$99.99")
        """
        if price is None or price == "":
            return "Not specified"
        
        try:
            price_float = float(price)
            return f"{settings.CURRENCY_SYMBOL}{price_float:,.{settings.DECIMAL_PLACES}f}"
        except (ValueError, TypeError):
            logger.warning(f"Could not format price: {price}")
            return "Invalid price"
    
    @staticmethod
    def format_price_range(min_price: Optional[float], max_price: Optional[float]) -> str:
        """
        Format price range
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            Formatted range string (e.g., "$10.00 - $99.99")
        """
        if min_price is None or maxprice is None:
            return "Price range not available"
        
        min_formatted = Formatter.format_price(min_price)
        max_formatted = Formatter.format_price(max_price)
        return f"{min_formatted} - {max_formatted}"
    
    # ========================================================================
    # DATE & TIME FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_date(date_obj: Optional[Union[datetime, date]]) -> str:
        """
        Format date as readable string
        
        Args:
            date_obj: Date or datetime object
            
        Returns:
            Formatted date string (e.g., "January 15, 2025")
        """
        if date_obj is None:
            return "Not specified"
        
        try:
            if isinstance(date_obj, str):
                date_obj = datetime.fromisoformat(date_obj).date()
            elif isinstance(date_obj, datetime):
                date_obj = date_obj.date()
            
            return date_obj.strftime(settings.DATE_FORMAT)
        except (ValueError, TypeError):
            logger.warning(f"Could not format date: {date_obj}")
            return "Invalid date"
    
    @staticmethod
    def format_datetime(dt_obj: Optional[datetime]) -> str:
        """
        Format datetime as readable string
        
        Args:
            dt_obj: Datetime object
            
        Returns:
            Formatted datetime string (e.g., "January 15, 2025 at 14:30:00")
        """
        if dt_obj is None:
            return "Not specified"
        
        try:
            if isinstance(dt_obj, str):
                dt_obj = datetime.fromisoformat(dt_obj)
            
            return dt_obj.strftime(settings.DATETIME_FORMAT)
        except (ValueError, TypeError):
            logger.warning(f"Could not format datetime: {dt_obj}")
            return "Invalid datetime"
    
    @staticmethod
    def format_time(time_obj: Optional[datetime]) -> str:
        """
        Format time only
        
        Args:
            time_obj: Datetime object
            
        Returns:
            Formatted time string (e.g., "14:30:00")
        """
        if time_obj is None:
            return "Not specified"
        
        try:
            if isinstance(time_obj, str):
                time_obj = datetime.fromisoformat(time_obj)
            
            return time_obj.strftime(settings.TIME_FORMAT)
        except (ValueError, TypeError):
            logger.warning(f"Could not format time: {time_obj}")
            return "Invalid time"
    
    @staticmethod
    def time_ago(dt_obj: Optional[datetime]) -> str:
        """
        Format datetime as relative time (e.g., "2 days ago")
        
        Args:
            dt_obj: Datetime object
            
        Returns:
            Relative time string
        """
        if dt_obj is None:
            return "Not specified"
        
        try:
            if isinstance(dt_obj, str):
                dt_obj = datetime.fromisoformat(dt_obj)
            elif isinstance(dt_obj, date) and not isinstance(dt_obj, datetime):
                dt_obj = datetime.combine(dt_obj, datetime.min.time())
            
            now = datetime.now()
            diff = now - dt_obj
            seconds = diff.total_seconds()
            
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif seconds < 604800:
                days = int(seconds / 86400)
                return f"{days} day{'s' if days > 1 else ''} ago"
            else:
                weeks = int(seconds / 604800)
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        except (ValueError, TypeError):
            return "Unknown time"
    
    # ========================================================================
    # NUMBER FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_number(number: Optional[Union[int, float]]) -> str:
        """
        Format number with thousand separators
        
        Args:
            number: Number to format
            
        Returns:
            Formatted number string (e.g., "1,234.56")
        """
        if number is None or number == "":
            return "Not specified"
        
        try:
            return f"{float(number):,.0f}"
        except (ValueError, TypeError):
            logger.warning(f"Could not format number: {number}")
            return "Invalid number"
    
    @staticmethod
    def format_percentage(value: Optional[float], decimal_places: int = 1) -> str:
        """
        Format number as percentage
        
        Args:
            value: Value to format as percentage
            decimal_places: Number of decimal places
            
        Returns:
            Formatted percentage string (e.g., "12.5%")
        """
        if value is None or value == "":
            return "Not specified"
        
        try:
            return f"{float(value):.{decimal_places}f}%"
        except (ValueError, TypeError):
            logger.warning(f"Could not format percentage: {value}")
            return "Invalid percentage"
    
    @staticmethod
    def format_percentage_change(old_value: Optional[float], new_value: Optional[float]) -> str:
        """
        Format percentage change with arrow indicator
        
        Args:
            old_value: Original value
            new_value: New value
            
        Returns:
            Formatted change string (e.g., "↑ 25.0%", "↓ 10.5%", "→ 0.0%")
        """
        if old_value is None or new_value is None or old_value == 0:
            return "N/A"
        
        try:
            old = float(old_value)
            new = float(new_value)
            
            if old == 0:
                return "N/A"
            
            change = ((new - old) / old) * 100
            
            if change > 0:
                arrow = "↑"
                color = "red"  # Price increase
            elif change < 0:
                arrow = "↓"
                color = "green"  # Price decrease
            else:
                arrow = "→"
                color = "gray"  # No change
            
            return f"{arrow} {abs(change):.1f}%"
        except (ValueError, TypeError):
            logger.warning(f"Could not format percentage change: {old_value} -> {new_value}")
            return "Invalid change"
    
    # ========================================================================
    # RATING FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_rating(rating: Optional[float], max_rating: float = 5.0) -> str:
        """
        Format rating with stars
        
        Args:
            rating: Rating value
            max_rating: Maximum rating value (default 5)
            
        Returns:
            Formatted rating string (e.g., "4.5 / 5.0 ⭐")
        """
        if rating is None or rating == "":
            return "Not rated"
        
        try:
            rating_float = float(rating)
            
            if rating_float < 0 or rating_float > max_rating:
                return "Invalid rating"
            
            stars = "⭐" * int(rating_float)
            return f"{rating_float:.1f} {MetricUnits.RATING} {stars}"
        except (ValueError, TypeError):
            logger.warning(f"Could not format rating: {rating}")
            return "Invalid rating"
    
    @staticmethod
    def get_rating_color(rating: Optional[float]) -> str:
        """
        Get color based on rating value
        
        Args:
            rating: Rating value (0-5)
            
        Returns:
            Color value
        """
        if rating is None:
            return Colors.NEUTRAL_400
        
        try:
            rating_float = float(rating)
            
            if rating_float >= 4.5:
                return Colors.ACCENT_TEAL  # Excellent
            elif rating_float >= 4.0:
                return Colors.ACCENT_BLUE  # Very good
            elif rating_float >= 3.0:
                return Colors.ACCENT_ORANGE  # Good
            else:
                return Colors.ACCENT_RED  # Poor
        except (ValueError, TypeError):
            return Colors.NEUTRAL_400
    
    # ========================================================================
    # SENTIMENT FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_sentiment(sentiment: Optional[str]) -> str:
        """
        Format sentiment with emoji
        
        Args:
            sentiment: Sentiment value (positive, neutral, negative)
            
        Returns:
            Formatted sentiment string (e.g., "😊 Positive")
        """
        if sentiment is None or sentiment == "":
            return "Not specified"
        
        try:
            sentiment_lower = sentiment.lower().strip()
            
            emoji_map = {
                Sentiments.POSITIVE: "😊",
                Sentiments.NEUTRAL: "😐",
                Sentiments.NEGATIVE: "😞"
            }
            
            emoji = emoji_map.get(sentiment_lower, "❓")
            return f"{emoji} {sentiment.capitalize()}"
        except:
            logger.warning(f"Could not format sentiment: {sentiment}")
            return sentiment
    
    @staticmethod
    def get_sentiment_color(sentiment: Optional[str]) -> str:
        """
        Get color based on sentiment
        
        Args:
            sentiment: Sentiment value
            
        Returns:
            Color value
        """
        if sentiment is None:
            return Colors.NEUTRAL_400
        
        sentiment_lower = sentiment.lower().strip()
        
        if sentiment_lower == Sentiments.POSITIVE:
            return Colors.ACCENT_TEAL
        elif sentiment_lower == Sentiments.NEGATIVE:
            return Colors.ACCENT_RED
        else:
            return Colors.NEUTRAL_400
    
    # ========================================================================
    # TEXT FORMATTING
    # ========================================================================
    
    @staticmethod
    def truncate(text: Optional[str], max_length: int = 50) -> str:
        """
        Truncate text to maximum length with ellipsis
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            
        Returns:
            Truncated text
        """
        if text is None or text == "":
            return "Not specified"
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def capitalize_words(text: Optional[str]) -> str:
        """
        Capitalize first letter of each word
        
        Args:
            text: Text to capitalize
            
        Returns:
            Capitalized text
        """
        if text is None or text == "":
            return "Not specified"
        
        return " ".join(word.capitalize() for word in text.split())
    
    @staticmethod
    def format_name(name: Optional[str]) -> str:
        """
        Format name (capitalize first letter)
        
        Args:
            name: Name to format
            
        Returns:
            Formatted name
        """
        if name is None or name == "":
            return "Unknown"
        
        return name.strip().capitalize()
    
    # ========================================================================
    # CATEGORY FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_category(category: Optional[str]) -> str:
        """
        Format category name
        
        Args:
            category: Category name
            
        Returns:
            Formatted category
        """
        if category is None or category == "":
            return "Other"
        
        return Formatter.capitalize_words(category)
    
    # ========================================================================
    # BILLING PERIOD FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_billing_period(period: Optional[str]) -> str:
        """
        Format billing period
        
        Args:
            period: Billing period (monthly, yearly, etc.)
            
        Returns:
            Formatted billing period
        """
        if period is None or period == "":
            return "Monthly"
        
        period_lower = period.lower().strip()
        
        format_map = {
            "monthly": "Monthly",
            "yearly": "Yearly",
            "per user/month": "Per User/Month",
            "per user/year": "Per User/Year",
            "one-time": "One-time",
            "custom": "Custom"
        }
        
        return format_map.get(period_lower, Formatter.capitalize_words(period))
    
    # ========================================================================
    # BADGE/LABEL FORMATTING
    # ========================================================================
    
    @staticmethod
    def get_status_badge_color(status: str) -> str:
        """
        Get color for status badge
        
        Args:
            status: Status value
            
        Returns:
            Color value
        """
        status_lower = status.lower()
        
        if "success" in status_lower or "active" in status_lower:
            return Colors.ACCENT_TEAL
        elif "pending" in status_lower or "warning" in status_lower:
            return Colors.ACCENT_ORANGE
        elif "error" in status_lower or "inactive" in status_lower:
            return Colors.ACCENT_RED
        else:
            return Colors.NEUTRAL_400
    
    # ========================================================================
    # LIST/ARRAY FORMATTING
    # ========================================================================
    
    @staticmethod
    def format_list(items: Optional[list], max_items: int = 3) -> str:
        """
        Format list as readable string
        
        Args:
            items: List of items
            max_items: Maximum items to show
            
        Returns:
            Formatted list string
        """
        if not items:
            return "None"
        
        displayed = items[:max_items]
        formatted = ", ".join(str(item) for item in displayed)
        
        if len(items) > max_items:
            formatted += f" +{len(items) - max_items} more"
        
        return formatted


# Global formatter instance for easy importing
formatter = Formatter()