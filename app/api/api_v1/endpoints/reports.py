from typing import List, Optional
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import json
import os

router = APIRouter()

@router.get("/traffic")
async def get_traffic_report(
    username: Optional[str] = None,
    period: str = Query("daily", regex="^(daily|weekly|monthly|yearly)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get traffic reports"""
    # Mock traffic report data
    if period == "daily":
        data = [
            {"date": "2024-01-01", "username": "user001", "rx_bytes": 1073741824, "tx_bytes": 536870912},
            {"date": "2024-01-02", "username": "user001", "rx_bytes": 2147483648, "tx_bytes": 1073741824},
            {"date": "2024-01-01", "username": "user002", "rx_bytes": 536870912, "tx_bytes": 268435456},
        ]
    elif period == "weekly":
        data = [
            {"week": "2024-W01", "username": "user001", "rx_bytes": 7516192768, "tx_bytes": 3758096384},
            {"week": "2024-W01", "username": "user002", "rx_bytes": 3758096384, "tx_bytes": 1879048192},
        ]
    elif period == "monthly":
        data = [
            {"month": "2024-01", "username": "user001", "rx_bytes": 32212254720, "tx_bytes": 16106127360},
            {"month": "2024-01", "username": "user002", "rx_bytes": 16106127360, "tx_bytes": 8053063680},
        ]
    else:  # yearly
        data = [
            {"year": "2024", "username": "user001", "rx_bytes": 386547056640, "tx_bytes": 193273528320},
            {"year": "2024", "username": "user002", "rx_bytes": 193273528320, "tx_bytes": 96636764160},
        ]
    
    if username:
        data = [d for d in data if d.get("username") == username]
    
    return {
        "period": period,
        "data": data,
        "total_records": len(data)
    }

@router.get("/billing")
async def get_billing_report(
    period: str = Query("monthly", regex="^(daily|weekly|monthly|yearly)$"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get billing reports"""
    # Mock billing report data
    return {
        "period": period,
        "total_revenue": 15750000,
        "paid_invoices": 45,
        "overdue_invoices": 5,
        "total_customers": 50,
        "new_customers": 3,
        "cancelled_customers": 1,
        "details": [
            {"date": "2024-01-01", "revenue": 5250000, "invoices_paid": 15},
            {"date": "2024-01-02", "revenue": 3500000, "invoices_paid": 10},
            {"date": "2024-01-03", "revenue": 7000000, "invoices_paid": 20},
        ]
    }

@router.get("/download/{report_type}")
async def download_report(
    report_type: str,
    period: str = Query("monthly"),
    format: str = Query("csv", regex="^(csv|xlsx|pdf)$")
):
    """Download report file"""
    # Mock file generation
    filename = f"{report_type}_{period}_report.{format}"
    
    # In production, generate actual report file
    mock_data = {
        "report_type": report_type,
        "period": period,
        "generated_at": datetime.now().isoformat(),
        "data": "Mock report data would be here"
    }
    
    # Create mock file
    os.makedirs("./reports", exist_ok=True)
    file_path = f"./reports/{filename}"
    
    if format == "csv":
        with open(file_path, "w") as f:
            f.write("Date,Username,RX Bytes,TX Bytes\n")
            f.write("2024-01-01,user001,1073741824,536870912\n")
            f.write("2024-01-02,user001,2147483648,1073741824\n")
    else:
        with open(file_path, "w") as f:
            json.dump(mock_data, f, indent=2)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )