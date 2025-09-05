from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from dependencies.mock_auth import get_current_user, require_admin, require_manage_users
from models.roles import UserRole, UserWithRole, Permission
from dependencies.mock_auth import set_user_role, get_user_role

router = APIRouter(prefix="/admin", tags=["admin-management"])

class UserRoleUpdate(BaseModel):
    uid: str
    role: UserRole

class UserRoleResponse(BaseModel):
    uid: str
    email: str
    role: UserRole
    permissions: List[str]

class SystemStats(BaseModel):
    total_users: int
    users_by_role: dict
    system_status: str

# In-memory storage for demo (replace with database)
all_users_db = []

@router.get("/users", response_model=List[UserRoleResponse])
async def get_all_users(current_user: UserWithRole = Depends(require_admin)):
    """Get all users with their roles (Admin only)"""
    # In a real app, this would query your user database
    users = []
    for uid, role in get_user_role.__globals__.get('user_roles_db', {}).items():
        users.append(UserRoleResponse(
            uid=uid,
            email=f"user_{uid}@example.com",  # This would come from your user database
            role=role,
            permissions=list(get_user_role.__globals__.get('ROLE_PERMISSIONS', {}).get(role, set()))
        ))
    return users

@router.put("/users/role", response_model=UserRoleResponse)
async def update_user_role(
    role_update: UserRoleUpdate,
    current_user: UserWithRole = Depends(require_manage_users)
):
    """Update user role (Admin and users with manage_users permission)"""
    set_user_role(role_update.uid, role_update.role)
    
    return UserRoleResponse(
        uid=role_update.uid,
        email=f"user_{role_update.uid}@example.com",
        role=role_update.role,
        permissions=list(get_user_role.__globals__.get('ROLE_PERMISSIONS', {}).get(role_update.role, set()))
    )

@router.get("/stats", response_model=SystemStats)
async def get_system_stats(current_user: UserWithRole = Depends(require_admin)):
    """Get system statistics (Admin only)"""
    user_roles_db = get_user_role.__globals__.get('user_roles_db', {})
    
    users_by_role = {}
    for role in UserRole:
        users_by_role[role.value] = sum(1 for user_role in user_roles_db.values() if user_role == role)
    
    return SystemStats(
        total_users=len(user_roles_db),
        users_by_role=users_by_role,
        system_status="healthy"
    )

@router.get("/permissions")
async def get_all_permissions(current_user: UserWithRole = Depends(require_admin)):
    """Get all available permissions (Admin only)"""
    return {
        "permissions": [permission.value for permission in Permission],
        "roles": {
            role.value: [perm.value for perm in perms] 
            for role, perms in get_user_role.__globals__.get('ROLE_PERMISSIONS', {}).items()
        }
    }

@router.delete("/users/{uid}")
async def delete_user(uid: str, current_user: UserWithRole = Depends(require_admin)):
    """Delete a user (Admin only)"""
    user_roles_db = get_user_role.__globals__.get('user_roles_db', {})
    if uid not in user_roles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # In a real app, you would delete from your user database
    del user_roles_db[uid]
    return {"message": f"User {uid} deleted successfully"}

@router.get("/logs")
async def get_system_logs(current_user: UserWithRole = Depends(require_admin)):
    """Get system logs (Admin only)"""
    # In a real app, this would query your logging system
    return {
        "logs": [
            {"timestamp": "2024-01-01T10:00:00Z", "level": "INFO", "message": "System started"},
            {"timestamp": "2024-01-01T10:01:00Z", "level": "INFO", "message": "User authenticated"},
        ]
    }
