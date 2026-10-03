from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChangeLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitor_id: int
    change_type: str
    summary: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    detected_at: datetime
    is_read: int