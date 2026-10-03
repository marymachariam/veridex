from typing import List, Optional

from pydantic import BaseModel


class BattlecardRead(BaseModel):
    competitor_id: int
    competitor_name: str
    one_liner: str
    why_we_win: List[str]
    watch_out_for: List[str]
    objection_handling: List[dict]  
    pricing_summary: str
    generated_at: str