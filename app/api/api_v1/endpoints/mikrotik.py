from typing import List, Any
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.mikrotik import MikroTikDevice, MikroTikDeviceCreate, MikroTikStats, InterfaceStats, PPPoEUser
from app.services.mikrotik_api import MikroTikAPI

router = APIRouter()

# Mock data for demonstration
mock_devices = [
    {
        "id": 1,
        "name": "MikroTik Main",
        "ip_address": "192.168.1.1",
        "port": 8728,
        "username": "admin",
        "description": "Main router for office",
        "is_active": True,
        "last_connected": None
    },
    {
        "id": 2,
        "name": "MikroTik Branch",
        "ip_address": "192.168.2.1",
        "port": 8728,
        "username": "admin",
        "description": "Branch office router",
        "is_active": True,
        "last_connected": None
    }
]

@router.get("/devices", response_model=List[MikroTikDevice])
async def get_mikrotik_devices():
    """Get all MikroTik devices"""
    return mock_devices

@router.post("/devices", response_model=MikroTikDevice)
async def create_mikrotik_device(device: MikroTikDeviceCreate):
    """Add new MikroTik device"""
    new_device = {
        "id": len(mock_devices) + 1,
        "name": device.name,
        "ip_address": device.ip_address,
        "port": device.port,
        "username": device.username,
        "description": device.description,
        "is_active": True,
        "last_connected": None
    }
    mock_devices.append(new_device)
    return new_device

@router.get("/devices/{device_id}/stats", response_model=MikroTikStats)
async def get_device_stats(device_id: int):
    """Get device statistics (CPU, memory, etc.)"""
    # Mock stats data
    return {
        "device_id": device_id,
        "cpu_load": 15.5,
        "memory_usage": 35.2,
        "uptime": "7d 14h 32m",
        "version": "6.49.6",
        "board_name": "RB4011iGS+",
        "architecture": "arm64"
    }

@router.get("/devices/{device_id}/interfaces", response_model=List[InterfaceStats])
async def get_interface_stats(device_id: int):
    """Get interface traffic statistics"""
    # Mock interface data
    return [
        {
            "name": "ether1",
            "rx_bytes": 1024000000,
            "tx_bytes": 512000000,
            "rx_packets": 1500000,
            "tx_packets": 1200000,
            "status": "running"
        },
        {
            "name": "ether2",
            "rx_bytes": 2048000000,
            "tx_bytes": 1024000000,
            "rx_packets": 2000000,
            "tx_packets": 1800000,
            "status": "running"
        }
    ]

@router.get("/devices/{device_id}/pppoe", response_model=List[PPPoEUser])
async def get_pppoe_users(device_id: int):
    """Get active PPPoE users"""
    # Mock PPPoE users
    return [
        {
            "name": "user001",
            "caller_id": "192.168.100.10",
            "address": "10.0.0.10",
            "uptime": "2d 5h 30m",
            "bytes_in": 1073741824,
            "bytes_out": 536870912,
            "service": "pppoe-service1"
        },
        {
            "name": "user002", 
            "caller_id": "192.168.100.11",
            "address": "10.0.0.11",
            "uptime": "1d 12h 15m",
            "bytes_in": 2147483648,
            "bytes_out": 1073741824,
            "service": "pppoe-service1"
        }
    ]

@router.get("/devices/{device_id}/pppoe/{username}/traffic")
async def get_user_traffic(device_id: int, username: str):
    """Get specific user traffic data"""
    # Mock user traffic data
    return {
        "username": username,
        "device_id": device_id,
        "daily_traffic": [
            {"date": "2024-01-01", "rx_bytes": 1073741824, "tx_bytes": 536870912},
            {"date": "2024-01-02", "rx_bytes": 2147483648, "tx_bytes": 1073741824},
        ],
        "weekly_traffic": [
            {"week": "2024-W01", "rx_bytes": 7516192768, "tx_bytes": 3758096384},
        ],
        "monthly_traffic": [
            {"month": "2024-01", "rx_bytes": 32212254720, "tx_bytes": 16106127360},
        ]
    }

@router.post("/devices/{device_id}/test-connection")
async def test_connection(device_id: int):
    """Test connection to MikroTik device"""
    device = next((d for d in mock_devices if d["id"] == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Mock connection test
    return {
        "success": True,
        "message": f"Successfully connected to {device['name']}",
        "response_time": "25ms"
    }