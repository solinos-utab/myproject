from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="PT MARS DATA TELEKOMUNIKASI - Network Management System with MikroTik API Integration, RADIUS Billing, and Traffic Monitoring",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to PT MARS DATA TELEKOMUNIKASI Network Management System",
        "version": "1.0.0",
        "features": [
            "MikroTik API Integration",
            "RADIUS Authentication & Billing",
            "Real-time Traffic Monitoring",
            "Automated Billing & Isolation",
            "Comprehensive Reporting",
            "User Role Management"
        ],
        "api_docs": "/docs",
        "api_version": settings.API_V1_STR
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "PT MARS DATA TELEKOMUNIKASI",
        "timestamp": "2024-01-01T00:00:00Z"
    }