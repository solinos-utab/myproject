from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MikroTikDeviceBase(BaseModel):
    name: str
    ip_address: str
    port: int = 8728
    username: str
    description: Optional[str] = None
    is_active: bool = True

class MikroTikDeviceCreate(MikroTikDeviceBase):
    password: str

class MikroTikDevice(MikroTikDeviceBase):
    id: int
    last_connected: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MikroTikStats(BaseModel):
    device_id: int
    cpu_load: float
    memory_usage: float
    uptime: str
    version: str
    board_name: str
    architecture: str

class InterfaceStats(BaseModel):
    name: str
    rx_bytes: int
    tx_bytes: int
    rx_packets: int
    tx_packets: int
    status: str

class PPPoEUser(BaseModel):
    name: str
    caller_id: str
    address: str
    uptime: str
    bytes_in: int
    bytes_out: int
    service: str