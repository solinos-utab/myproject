from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RadiusUserBase(BaseModel):
    username: str
    billing_account_id: int
    group_name: str
    is_active: bool = True

class RadiusUserCreate(RadiusUserBase):
    password: str

class RadiusUser(RadiusUserBase):
    id: int
    created_at: datetime
    last_activity: Optional[datetime] = None

    class Config:
        orm_mode = True