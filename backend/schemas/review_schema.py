from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.constants import Sentiment


class ReviewCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    competitor_id: int
    source: str = Field(default="Manual", min_length=1, max_length=50)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    sentiment: Optional[Sentiment] = None
    comment_summary: Optional[str] = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def _derive_sentiment(self):
        if self.sentiment is None:
            if self.rating is None:
                self.sentiment = "neutral"
            elif self.rating >= 4:
                self.sentiment = "positive"
            elif self.rating <= 2:
                self.sentiment = "negative"
            else:
                self.sentiment = "neutral"
        return self


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    source: str
    rating: Optional[float] = None
    sentiment: str
    comment_summary: Optional[str] = None
    recorded_date: datetime