from fastapi import APIRouter, Depends
from schemas.usage import UsageList
from services.usage_service import UsageService

router = APIRouter()

usage_service_singleton: UsageService = UsageService()

def get_usage_service() -> UsageService:
    return usage_service_singleton

@router.get("/usage", response_model=UsageList)
async def get_usage_for_current_period(usage_service: UsageService = Depends(get_usage_service)):
    usage_list: UsageList = usage_service.get_usage_for_current_period()
    return usage_list
