from pydantic import BaseModel
from typing import List, Optional

class Report(BaseModel):
    name: Optional[str]
    credit_cost: float
    id: int 
