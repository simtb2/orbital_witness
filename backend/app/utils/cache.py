from typing import Dict, Optional
from schemas.usage import UsageList

class Cache:
    def __init__(self):
        self.cache: Dict[str, Optional[UsageList]] = dict()
    
    def get(self, key: str) -> UsageList:
        value: Optional[UsageList] = self.cache.get(key)
        return value

    def set(self, key: str, value: UsageList) -> None:
        self.cache[key] = value
