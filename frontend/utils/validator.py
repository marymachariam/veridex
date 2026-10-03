class Validator:
    @staticmethod
    def validate_tier_name(name):
        if not name or len(name) < 2:
            return False, "Tier name required (min 2 chars)"
        return True, ""
    
    @staticmethod
    def validate_description(desc):
        if desc and len(desc) > 500:
            return False, "Description too long (max 500 chars)"
        return True, ""
    
    @staticmethod
    def validate_comment(comment):
        if comment and len(comment) > 1000:
            return False, "Comment too long (max 1000 chars)"
        return True, ""
    
    @staticmethod
    def validate_price_change(old, new):
        if old < 0 or new < 0:
            return False, "Prices cannot be negative"
        return True, ""

validator = Validator()
