from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FeatureCreate(BaseModel):
    competitor_id: int
    feature_name: str = Field(min_length=1, max_length=255)
    tier_available: Optional[str] = Field(default=None, max_length=100)


class FeatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    feature_name: str
    tier_available: Optional[str] = None
    recorded_date: datetime