from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BillingAccountBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    package_name: str
    package_price: float
    bandwidth_profile: str
    status: str = "active"
    due_date: datetime

class BillingAccountCreate(BillingAccountBase):
    pass

class BillingAccount(BillingAccountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    billing_account_id: int
    amount: float
    payment_method: str
    due_date: datetime
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: str
    payment_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True

class BillingStats(BaseModel):
    total_accounts: int
    active_accounts: int
    suspended_accounts: int
    paid_accounts: int
    overdue_accounts: int
    total_revenue: float
    pending_revenue: float