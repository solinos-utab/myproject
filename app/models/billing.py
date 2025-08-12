from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class BillingStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class BillingAccount(Base):
    __tablename__ = "billing_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    package_name = Column(String(100), nullable=False)
    package_price = Column(Float, nullable=False)
    bandwidth_profile = Column(String(50), nullable=False)
    status = Column(Enum(BillingStatus), default=BillingStatus.ACTIVE)
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    billing_account_id = Column(Integer, ForeignKey("billing_accounts.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrafficData(Base):
    __tablename__ = "traffic_data"
    
    id = Column(Integer, primary_key=True, index=True)
    billing_account_id = Column(Integer, ForeignKey("billing_accounts.id"))
    mikrotik_device_id = Column(Integer, ForeignKey("mikrotik_devices.id"))
    username = Column(String(50), nullable=False)
    rx_bytes = Column(Integer, default=0)
    tx_bytes = Column(Integer, default=0)
    total_bytes = Column(Integer, default=0)
    session_time = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    date_only = Column(String(10), nullable=False)  # YYYY-MM-DD for easy grouping