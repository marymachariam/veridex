from models.change_log import ChangeLog
from models.competitor import Competitor
from models.feature import Feature
from models.insight import CompetitorInsight
from models.price_history import PriceHistory
from models.pricing import Pricing
from models.review import Review

from .tenant_repo import TenantRepository

competitor_repo = TenantRepository(Competitor)
pricing_repo = TenantRepository(Pricing)
review_repo = TenantRepository(Review)
feature_repo = TenantRepository(Feature)
price_history_repo = TenantRepository(PriceHistory)
insight_repo = TenantRepository(CompetitorInsight)
change_log_repo = TenantRepository(ChangeLog)