from typing import List
from fastapi import APIRouter
from app.schemas.radius import RadiusUser, RadiusUserCreate

router = APIRouter()

# Mock RADIUS users data
mock_radius_users = [
    {
        "id": 1,
        "username": "user001",
        "billing_account_id": 1,
        "group_name": "premium_users",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "last_activity": "2024-01-15T14:30:00"
    },
    {
        "id": 2,
        "username": "user002",
        "billing_account_id": 2,
        "group_name": "basic_users",
        "is_active": False,
        "created_at": "2024-01-01T00:00:00",
        "last_activity": "2024-01-10T09:15:00"
    }
]

@router.get("/users", response_model=List[RadiusUser])
async def get_radius_users():
    """Get all RADIUS users"""
    return mock_radius_users

@router.post("/users", response_model=RadiusUser)
async def create_radius_user(user: RadiusUserCreate):
    """Create new RADIUS user"""
    new_user = {
        "id": len(mock_radius_users) + 1,
        "username": user.username,
        "billing_account_id": user.billing_account_id,
        "group_name": user.group_name,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "last_activity": None
    }
    mock_radius_users.append(new_user)
    return new_user

@router.post("/users/{user_id}/activate")
async def activate_radius_user(user_id: int):
    """Activate RADIUS user"""
    user = next((u for u in mock_radius_users if u["id"] == user_id), None)
    if user:
        user["is_active"] = True
        return {"message": f"User {user['username']} activated"}
    return {"error": "User not found"}

@router.post("/users/{user_id}/deactivate")
async def deactivate_radius_user(user_id: int):
    """Deactivate RADIUS user"""
    user = next((u for u in mock_radius_users if u["id"] == user_id), None)
    if user:
        user["is_active"] = False
        return {"message": f"User {user['username']} deactivated"}
    return {"error": "User not found"}