from datetime import datetime, timedelta
from typing import List, Dict, Optional
import schedule
import time
from sqlalchemy.orm import Session

class BillingService:
    """Billing and Payment Management Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def process_overdue_accounts(self) -> List[Dict]:
        """Process overdue accounts and isolate them"""
        overdue_accounts = []
        current_date = datetime.now()
        
        # Mock implementation - in production, query database
        mock_accounts = [
            {
                "id": 1,
                "username": "user001",
                "due_date": "2024-01-15",
                "status": "active",
                "amount_due": 350000
            },
            {
                "id": 2,
                "username": "user002", 
                "due_date": "2024-01-10",
                "status": "active",
                "amount_due": 200000
            }
        ]
        
        for account in mock_accounts:
            due_date = datetime.fromisoformat(account["due_date"])
            if due_date < current_date and account["status"] == "active":
                # Mark as overdue and isolate
                account["status"] = "suspended"
                overdue_accounts.append({
                    "account_id": account["id"],
                    "username": account["username"],
                    "days_overdue": (current_date - due_date).days,
                    "amount_due": account["amount_due"],
                    "action": "isolated"
                })
        
        return overdue_accounts
    
    def generate_monthly_invoices(self) -> List[Dict]:
        """Generate monthly invoices for all active accounts"""
        invoices = []
        current_date = datetime.now()
        next_month = current_date + timedelta(days=30)
        
        # Mock active accounts
        active_accounts = [
            {
                "id": 1,
                "username": "user001",
                "package_price": 350000,
                "package_name": "Premium 50Mbps"
            },
            {
                "id": 2,
                "username": "user002",
                "package_price": 200000,
                "package_name": "Basic 25Mbps"
            }
        ]
        
        for account in active_accounts:
            invoice = {
                "account_id": account["id"],
                "username": account["username"],
                "amount": account["package_price"],
                "package": account["package_name"],
                "invoice_date": current_date.isoformat(),
                "due_date": next_month.isoformat(),
                "status": "pending"
            }
            invoices.append(invoice)
        
        return invoices
    
    def process_payment(self, account_id: int, amount: float, 
                       payment_method: str, reference: str = None) -> Dict:
        """Process payment for an account"""
        # Mock payment processing
        payment = {
            "payment_id": f"PAY_{int(time.time())}",
            "account_id": account_id,
            "amount": amount,
            "payment_method": payment_method,
            "reference": reference,
            "status": "completed",
            "processed_at": datetime.now().isoformat()
        }
        
        # In production: update database, send receipt, reactivate account if needed
        
        return payment
    
    def get_revenue_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate revenue report for date range"""
        # Mock revenue data
        total_revenue = 15750000
        total_payments = 45
        average_payment = total_revenue / total_payments if total_payments > 0 else 0
        
        return {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "total_revenue": total_revenue,
            "total_payments": total_payments,
            "average_payment": average_payment,
            "payment_methods": {
                "bank_transfer": {"count": 25, "amount": 8750000},
                "cash": {"count": 15, "amount": 5250000},
                "e_wallet": {"count": 5, "amount": 1750000}
            },
            "daily_breakdown": [
                {"date": "2024-01-01", "revenue": 3500000, "payments": 10},
                {"date": "2024-01-02", "revenue": 2800000, "payments": 8},
                {"date": "2024-01-03", "revenue": 4200000, "payments": 12},
                {"date": "2024-01-04", "revenue": 2450000, "payments": 7},
                {"date": "2024-01-05", "revenue": 2800000, "payments": 8}
            ]
        }
    
    def schedule_auto_isolation(self):
        """Schedule automatic isolation of overdue accounts"""
        schedule.every().day.at("02:00").do(self.process_overdue_accounts)
        schedule.every().month.at("01:00").do(self.generate_monthly_invoices)
    
    def get_account_status(self, username: str) -> Dict:
        """Get account status and payment history"""
        # Mock account data
        return {
            "username": username,
            "status": "active",
            "current_balance": 350000,
            "last_payment": "2024-01-15T10:30:00",
            "next_due_date": "2024-02-15T23:59:59",
            "package": "Premium 50Mbps",
            "traffic_usage": {
                "daily_limit": 0,  # unlimited
                "monthly_usage": 25600000000,  # 25GB
                "remaining_days": 15
            }
        }