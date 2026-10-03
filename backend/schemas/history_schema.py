from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: int
    competitor_id: Optional[int] = None
    competitor_name: str
    website: Optional[str] = None
    category: Optional[str] = None
    created_at: datetime
    run_by: Optional[str] = None
    summary: Optional[str] = None


class HistoryDetail(BaseModel):
    id: int
    competitor_id: Optional[int] = None
    competitor_name: str
    website: Optional[str] = None
    category: Optional[str] = None
    created_at: datetime
    run_by: Optional[str] = None
    result: Dict[str, Any]