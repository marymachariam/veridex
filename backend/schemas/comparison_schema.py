from typing import List, Optional

from pydantic import BaseModel, Field

from schemas.competitor_schema import CompetitorRead
from schemas.feature_schema import FeatureRead
from schemas.pricing_schema import PricingRead
from schemas.research_schema import InsightRead


class ComparisonRequest(BaseModel):
    competitor_ids: List[int] = Field(min_length=2, max_length=4)


class CompetitorComparisonEntry(BaseModel):
    competitor: CompetitorRead
    pricing: List[PricingRead]
    features: List[FeatureRead]
    insight: Optional[InsightRead] = None


class ComparisonResponse(BaseModel):
    competitors: List[CompetitorComparisonEntry]