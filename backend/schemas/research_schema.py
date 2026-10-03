from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    website: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)

class PricingTierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tier_name: str
    price_usd: Optional[float] = None
    billing_period: str = "monthly"
    description: Optional[str] = None


class FeatureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    feature_name: str
    tier_available: Optional[str] = None


class InsightRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tagline: Optional[str] = None
    target_market: Optional[str] = None
    summary: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    opportunities: Optional[str] = None
    threats: Optional[str] = None
    recent_signals: Optional[str] = None
    sources: Optional[str] = None
    researched_at: datetime


class ResearchReport(BaseModel):
    competitor_id: int
    name: str
    category: Optional[str] = None
    website: Optional[str] = None
    founded_year: Optional[int] = None
    pricing: List[PricingTierOut] = []
    features: List[FeatureOut] = []
    insight: Optional[InsightRead] = None