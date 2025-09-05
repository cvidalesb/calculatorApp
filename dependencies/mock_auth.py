from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models.roles import UserRole, UserWithRole, get_user_permissions
import uuid

security = HTTPBearer(auto_error=False)  # Don't auto-raise error if no token

# Mock user database for development
mock_users_db = {
    "admin_user": {
        "uid": "admin_user",
        "email": "admin@example.com",
        "display_name": "Admin User",
        "role": UserRole.ADMIN
    },
    "stakeholder_user": {
        "uid": "stakeholder_user", 
        "email": "stakeholder@example.com",
        "display_name": "Stakeholder User",
        "role": UserRole.STAKEHOLDER
    },
    "internal_user": {
        "uid": "internal_user",
        "email": "internal@example.com", 
        "display_name": "Internal User",
        "role": UserRole.INTERNAL
    },
    "normal_user": {
        "uid": "normal_user",
        "email": "normal@example.com",
        "display_name": "Normal User", 
        "role": UserRole.NORMAL
    }
}

def get_user_role(uid: str) -> UserRole:
    """Get user role from mock database"""
    user = mock_users_db.get(uid)
    return user["role"] if user else UserRole.NORMAL

def set_user_role(uid: str, role: UserRole):
    """Set user role in mock database"""
    if uid in mock_users_db:
        mock_users_db[uid]["role"] = role

async def verify_mock_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Mock token verification - just return user info based on token"""
    if not credentials:
        # Default to normal user if no token provided
        return {
            "uid": "normal_user",
            "email": "normal@example.com",
            "email_verified": True,
            "name": "Normal User"
        }
    
    # Extract user type from token (format: "Bearer user_type")
    token = credentials.credentials
    user_type = token.lower()
    
    if user_type in mock_users_db:
        user_data = mock_users_db[user_type]
        return {
            "uid": user_data["uid"],
            "email": user_data["email"],
            "email_verified": True,
            "name": user_data["display_name"]
        }
    else:
        # Default to normal user for unknown tokens
        return {
            "uid": "normal_user",
            "email": "normal@example.com", 
            "email_verified": True,
            "name": "Normal User"
        }

async def get_current_user(token_data: dict = Depends(verify_mock_token)) -> UserWithRole:
    """Get current authenticated user with role information"""
    uid = token_data["uid"]
    user_role = get_user_role(uid)
    
    return UserWithRole(
        uid=uid,
        email=token_data.get("email", ""),
        email_verified=token_data.get("email_verified", False),
        display_name=token_data.get("name", ""),
        role=user_role,
        permissions=get_user_permissions(user_role)
    )

def require_permission(permission):
    """Dependency factory for requiring specific permissions"""
    async def permission_checker(current_user: UserWithRole = Depends(get_current_user)):
        if permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission}"
            )
        return current_user
    return permission_checker

def require_role(required_role: UserRole):
    """Dependency factory for requiring specific roles"""
    async def role_checker(current_user: UserWithRole = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role. Required: {required_role}"
            )
        return current_user
    return role_checker

def require_any_role(*required_roles: UserRole):
    """Dependency factory for requiring any of the specified roles"""
    async def role_checker(current_user: UserWithRole = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role. Required one of: {', '.join(required_roles)}"
            )
        return current_user
    return role_checker

# Common role-based dependencies
require_admin = require_role(UserRole.ADMIN)
require_stakeholder_or_admin = require_any_role(UserRole.STAKEHOLDER, UserRole.ADMIN)
require_internal_or_above = require_any_role(UserRole.INTERNAL, UserRole.STAKEHOLDER, UserRole.ADMIN)

# Permission-based dependencies
from models.roles import Permission
require_manage_users = require_permission(Permission.MANAGE_USERS)
require_view_all_data = require_permission(Permission.VIEW_ALL_DATA)
require_edit_all_data = require_permission(Permission.EDIT_ALL_DATA)
require_view_analytics = require_permission(Permission.VIEW_ANALYTICS)
