from fastapi import APIRouter

from app.api.endpoints import atm

api_router = APIRouter()

api_router.include_router(atm.router, prefix="/atm", tags=["atm"])
