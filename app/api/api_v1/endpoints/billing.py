from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.billing import BillingAccount, BillingAccountCreate, Payment, PaymentCreate, BillingStats

router = APIRouter()

# Mock billing data
mock_accounts = [
    {
        "id": 1,
        "username": "user001",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "081234567890",
        "package_name": "Premium 50Mbps",
        "package_price": 350000,
        "bandwidth_profile": "50M/50M",
        "status": "active",
        "due_date": "2024-02-01T00:00:00",
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "username": "user002",
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "081234567891",
        "package_name": "Basic 25Mbps",
        "package_price": 200000,
        "bandwidth_profile": "25M/25M",
        "status": "suspended",
        "due_date": "2024-01-15T00:00:00",
        "created_at": "2024-01-01T00:00:00"
    }
]

mock_payments = [
    {
        "id": 1,
        "billing_account_id": 1,
        "amount": 350000,
        "payment_method": "Bank Transfer",
        "status": "paid",
        "payment_date": "2024-01-28T10:30:00",
        "due_date": "2024-02-01T00:00:00",
        "notes": "Payment received on time"
    },
    {
        "id": 2,
        "billing_account_id": 2,
        "amount": 200000,
        "payment_method": "Cash",
        "status": "overdue",
        "payment_date": None,
        "due_date": "2024-01-15T00:00:00",
        "notes": "Payment overdue - account suspended"
    }
]

@router.get("/accounts", response_model=List[BillingAccount])
async def get_billing_accounts():
    """Get all billing accounts"""
    return mock_accounts

@router.post("/accounts", response_model=BillingAccount)
async def create_billing_account(account: BillingAccountCreate):
    """Create new billing account"""
    new_account = {
        "id": len(mock_accounts) + 1,
        "username": account.username,
        "full_name": account.full_name,
        "email": account.email,
        "phone": account.phone,
        "package_name": account.package_name,
        "package_price": account.package_price,
        "bandwidth_profile": account.bandwidth_profile,
        "status": "active",
        "due_date": account.due_date,
        "created_at": "2024-01-01T00:00:00"
    }
    mock_accounts.append(new_account)
    return new_account

@router.get("/payments", response_model=List[Payment])
async def get_payments():
    """Get all payments"""
    return mock_payments

@router.post("/payments", response_model=Payment)
async def create_payment(payment: PaymentCreate):
    """Record new payment"""
    new_payment = {
        "id": len(mock_payments) + 1,
        "billing_account_id": payment.billing_account_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "status": "paid",
        "payment_date": "2024-01-01T00:00:00",
        "due_date": payment.due_date,
        "notes": payment.notes
    }
    mock_payments.append(new_payment)
    return new_payment

@router.get("/stats", response_model=BillingStats)
async def get_billing_stats():
    """Get billing statistics"""
    total_accounts = len(mock_accounts)
    paid_accounts = len([p for p in mock_payments if p["status"] == "paid"])
    overdue_accounts = len([p for p in mock_payments if p["status"] == "overdue"])
    total_revenue = sum([p["amount"] for p in mock_payments if p["status"] == "paid"])
    
    return {
        "total_accounts": total_accounts,
        "active_accounts": len([a for a in mock_accounts if a["status"] == "active"]),
        "suspended_accounts": len([a for a in mock_accounts if a["status"] == "suspended"]),
        "paid_accounts": paid_accounts,
        "overdue_accounts": overdue_accounts,
        "total_revenue": total_revenue,
        "pending_revenue": sum([p["amount"] for p in mock_payments if p["status"] == "overdue"])
    }

@router.post("/accounts/{account_id}/isolate")
async def isolate_account(account_id: int):
    """Isolate account for non-payment"""
    account = next((a for a in mock_accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account["status"] = "suspended"
    return {"message": f"Account {account['username']} has been isolated"}

@router.post("/accounts/{account_id}/reactivate")
async def reactivate_account(account_id: int):
    """Reactivate suspended account"""
    account = next((a for a in mock_accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account["status"] = "active"
    return {"message": f"Account {account['username']} has been reactivated"}