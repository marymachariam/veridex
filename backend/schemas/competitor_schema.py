import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _clean_website(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    v = re.sub(r"^https?://", "", v.strip(), flags=re.I).rstrip("/")
    return v or None


def _clean_name(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    v = v.strip()
    if not v:
        raise ValueError("Name cannot be empty")
    return v


class CompetitorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(default="Other", max_length=100)
    website: Optional[str] = Field(default=None, max_length=255)
    founded_year: Optional[int] = Field(default=None, ge=1800, le=2100)

    _v_name = field_validator("name")(_clean_name)
    _v_site = field_validator("website")(_clean_website)


class CompetitorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=255)
    founded_year: Optional[int] = Field(default=None, ge=1800, le=2100)

    _v_name = field_validator("name")(_clean_name)
    _v_site = field_validator("website")(_clean_website)


class CompetitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: Optional[str] = None
    website: Optional[str] = None
    founded_year: Optional[int] = None
    created_at: datetime
    updated_at: datetime