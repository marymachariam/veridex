from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PriceHistoryCreate(BaseModel):
    competitor_id: int
    tier_name: str = Field(min_length=1, max_length=100)
    old_price: Optional[float] = Field(default=None, ge=0)
    new_price: Optional[float] = Field(default=None, ge=0)
    change_date: Optional[datetime] = None

    @field_validator("change_date")
    @classmethod
    def _to_naive_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v.tzinfo is not None:
            return v.astimezone(timezone.utc).replace(tzinfo=None)
        return v

    @model_validator(mode="after")
    def _need_a_price(self):
        if self.old_price is None and self.new_price is None:
            raise ValueError("Provide old_price and/or new_price")
        return self


class PriceHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    tier_name: str
    old_price: Optional[float] = None
    new_price: Optional[float] = None
    change_date: datetime
    change_percent: Optional[float] = None