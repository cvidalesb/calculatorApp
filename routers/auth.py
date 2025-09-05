from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from dependencies.mock_auth import get_current_user
from models.roles import UserWithRole

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models
class AuthInfo(BaseModel):
    uid: str
    email: str
    email_verified: bool
    display_name: str = None
    role: str
    permissions: list

# Public endpoints
@router.get("/health")
async def auth_health():
    return {
        "status": "healthy",
        "auth_type": "mock_authentication",
        "message": "Mock authentication is active for development"
    }

# Protected endpoints (require authentication)
@router.get("/me", response_model=AuthInfo)
async def get_current_user_info(current_user: UserWithRole = Depends(get_current_user)):
    """Get current authenticated user information"""
    return AuthInfo(
        uid=current_user.uid,
        email=current_user.email,
        email_verified=current_user.email_verified,
        display_name=current_user.display_name,
        role=current_user.role.value,
        permissions=[perm.value for perm in current_user.permissions]
    )

@router.get("/verify")
async def verify_token(current_user: UserWithRole = Depends(get_current_user)):
    """Verify if the provided token is valid"""
    return {
        "valid": True,
        "user": {
            "uid": current_user.uid,
            "email": current_user.email,
            "role": current_user.role.value,
            "permissions": [perm.value for perm in current_user.permissions]
        },
        "message": "Token is valid"
    }

@router.get("/mock-users")
async def get_mock_users():
    """Get list of available mock users for testing"""
    return {
        "message": "Use these tokens in Authorization header for testing:",
        "users": [
            {"token": "admin_user", "role": "admin", "description": "Full access"},
            {"token": "stakeholder_user", "role": "stakeholder", "description": "High access"},
            {"token": "internal_user", "role": "internal", "description": "Limited access"},
            {"token": "normal_user", "role": "normal", "description": "Basic access"},
            {"token": "any_other_token", "role": "normal", "description": "Default to normal user"}
        ],
        "usage": "Authorization: Bearer <token>"
    }
