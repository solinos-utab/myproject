from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MikroTikDevice(Base):
    __tablename__ = "mikrotik_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(15), unique=True, nullable=False)
    port = Column(Integer, default=8728)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean(), default=True)
    last_connected = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)