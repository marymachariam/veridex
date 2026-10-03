from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from core.constants import BillingPeriod


class PricingCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    competitor_id: int
    tier_name: str = Field(min_length=1, max_length=100)
    price_usd: Optional[float] = Field(default=None, ge=0)
    billing_period: BillingPeriod = Field(default=BillingPeriod.MONTHLY, validate_default=True)
    description: Optional[str] = Field(default=None, max_length=1000)


class PricingUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    tier_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    price_usd: Optional[float] = Field(default=None, ge=0)
    billing_period: Optional[BillingPeriod] = None
    description: Optional[str] = Field(default=None, max_length=1000)


class PricingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    tier_name: str
    price_usd: Optional[float] = None
    billing_period: str
    description: Optional[str] = None
    recorded_date: datetime