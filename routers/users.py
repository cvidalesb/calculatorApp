from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from dependencies.mock_auth import get_current_user, require_view_all_users
from models.roles import UserWithRole, UserRole

router = APIRouter(prefix="/users", tags=["user-management"])

# User-specific models
class UserProfile(BaseModel):
    uid: str
    email: str
    display_name: str = None
    email_verified: bool
    preferences: dict = {}

class UpdateProfile(BaseModel):
    display_name: Optional[str] = None
    preferences: Optional[dict] = None

# In-memory storage for user profiles (replace with database)
user_profiles_db = {}

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: UserWithRole = Depends(get_current_user)):
    """Get current user's profile"""
    profile = user_profiles_db.get(current_user.uid, {
        "uid": current_user.uid,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "email_verified": current_user.email_verified,
        "preferences": {}
    })
    return profile

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UpdateProfile,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Update current user's profile"""
    current_profile = user_profiles_db.get(current_user.uid, {
        "uid": current_user.uid,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "email_verified": current_user.email_verified,
        "preferences": {}
    })
    
    if profile_update.display_name is not None:
        current_profile["display_name"] = profile_update.display_name
    if profile_update.preferences is not None:
        current_profile["preferences"].update(profile_update.preferences)
    
    user_profiles_db[current_user.uid] = current_profile
    return current_profile

@router.get("/dashboard")
async def get_user_dashboard(current_user: UserWithRole = Depends(get_current_user)):
    """Get user dashboard data"""
    return {
        "user": current_user,
        "profile": user_profiles_db.get(current_user.uid, {}),
        "stats": {
            "total_data_items": 0,  # This would come from your data router
            "last_login": "2024-01-01T00:00:00Z"
        }
    }
