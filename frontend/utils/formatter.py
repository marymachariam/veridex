class Formatter:
    @staticmethod
    def format_price(price):
        return f"${price:,.2f}" if price else "N/A"
    
    @staticmethod
    def format_rating(rating):
        return f"⭐ {rating}/5" if rating else "N/A"
    
    @staticmethod
    def format_date(date):
        return str(date) if date else "N/A"
    
    @staticmethod
    def format_sentiment(sentiment):
        colors = {"positive": "🟢", "neutral": "🟡", "negative": "🔴"}
        return f"{colors.get(sentiment, '⚪')} {sentiment}" if sentiment else "N/A"
    
    @staticmethod
    def format_percentage(value):
        return f"{value:.1f}%"
    
    @staticmethod
    def format_percentage_change(old, new):
        if old <= 0:
            return "N/A"
        change = ((new - old) / old) * 100
        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
        return f"{arrow} {change:+.1f}%"

formatter = Formatter()
