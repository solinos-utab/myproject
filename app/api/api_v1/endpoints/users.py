from typing import List
from fastapi import APIRouter
from app.schemas.user import User, UserCreate

router = APIRouter()

# Mock users data
mock_users = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@marsdata.com",
        "full_name": "Administrator",
        "role": "admin",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "username": "operator1",
        "email": "operator1@marsdata.com", 
        "full_name": "Network Operator",
        "role": "operator",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00"
    }
]

@router.get("/", response_model=List[User])
async def get_users():
    """Get all users"""
    return mock_users

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Create new user"""
    new_user = {
        "id": len(mock_users) + 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00"
    }
    mock_users.append(new_user)
    return new_user