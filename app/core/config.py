from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PT MARS DATA TELEKOMUNIKASI - Network Management System"
    
    # Database
    DATABASE_URL: str = "sqlite:///./mars_data.db"
    
    # Security
    SECRET_KEY: str = "mars-data-telekomunikasi-secret-key-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # MikroTik API Settings
    MIKROTIK_DEFAULT_PORT: int = 8728
    MIKROTIK_API_TIMEOUT: int = 10
    
    # RADIUS Settings
    RADIUS_SECRET: str = "mars-radius-secret"
    RADIUS_AUTH_PORT: int = 1812
    RADIUS_ACCT_PORT: int = 1813
    
    # Billing Settings
    BILLING_CURRENCY: str = "IDR"
    BILLING_TIMEZONE: str = "Asia/Jakarta"
    
    # Report Settings
    REPORT_STORAGE_PATH: str = "./reports"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()