from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, mikrotik, billing, radius, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(mikrotik.router, prefix="/mikrotik", tags=["mikrotik"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(radius.router, prefix="/radius", tags=["radius"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])