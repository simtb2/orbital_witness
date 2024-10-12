from pydantic import BaseModel
from typing import List, Optional

class Usage(BaseModel):
    message_id: int
    timestamp: str
    report_name: Optional[str]
    credits_used: float

class UsageList(BaseModel):
    usage: List[Usage]