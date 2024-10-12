from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    text: str
    timestamp: datetime
    report_id: Optional[int] = None
    id: int
