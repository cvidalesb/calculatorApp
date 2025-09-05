from enum import Enum
from typing import List, Dict, Set
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    STAKEHOLDER = "stakeholder"
    INTERNAL = "internal"
    NORMAL = "normal"

class Permission(str, Enum):
    # User management permissions
    MANAGE_USERS = "manage_users"
    VIEW_ALL_USERS = "view_all_users"
    EDIT_USER_ROLES = "edit_user_roles"
    
    # Data permissions
    VIEW_ALL_DATA = "view_all_data"
    EDIT_ALL_DATA = "edit_all_data"
    DELETE_ALL_DATA = "delete_all_data"
    
    # Analytics/Reports permissions
    VIEW_ANALYTICS = "view_analytics"
    EXPORT_DATA = "export_data"
    
    # System permissions
    VIEW_SYSTEM_LOGS = "view_system_logs"
    MANAGE_SYSTEM_SETTINGS = "manage_system_settings"

# Role-based permissions mapping
ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
    UserRole.ADMIN: {
        # Admin has access to everything
        Permission.MANAGE_USERS,
        Permission.VIEW_ALL_USERS,
        Permission.EDIT_USER_ROLES,
        Permission.VIEW_ALL_DATA,
        Permission.EDIT_ALL_DATA,
        Permission.DELETE_ALL_DATA,
        Permission.VIEW_ANALYTICS,
        Permission.EXPORT_DATA,
        Permission.VIEW_SYSTEM_LOGS,
        Permission.MANAGE_SYSTEM_SETTINGS,
    },
    
    UserRole.STAKEHOLDER: {
        # Stakeholder has access to most things except system management
        Permission.VIEW_ALL_USERS,
        Permission.VIEW_ALL_DATA,
        Permission.EDIT_ALL_DATA,
        Permission.VIEW_ANALYTICS,
        Permission.EXPORT_DATA,
    },
    
    UserRole.INTERNAL: {
        # Internal user has limited access
        Permission.VIEW_ALL_USERS,
        Permission.VIEW_ALL_DATA,
        Permission.VIEW_ANALYTICS,
    },
    
    UserRole.NORMAL: {
        # Normal user only has access to their own data
        # No additional permissions beyond basic user operations
    }
}

class UserWithRole(BaseModel):
    uid: str
    email: str
    email_verified: bool
    display_name: str = None
    role: UserRole
    permissions: Set[Permission]

def get_user_permissions(role: UserRole) -> Set[Permission]:
    """Get permissions for a specific role"""
    return ROLE_PERMISSIONS.get(role, set())

def has_permission(user_role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(user_role, set())

def can_access_user_data(user_role: UserRole, data_owner_id: str, current_user_id: str) -> bool:
    """Check if user can access specific data"""
    if user_role == UserRole.ADMIN or user_role == UserRole.STAKEHOLDER:
        return True  # Can access all data
    elif user_role == UserRole.INTERNAL:
        return True  # Can view all data but not edit
    else:
        return data_owner_id == current_user_id  # Normal users can only access their own data

def can_edit_user_data(user_role: UserRole, data_owner_id: str, current_user_id: str) -> bool:
    """Check if user can edit specific data"""
    if user_role == UserRole.ADMIN or user_role == UserRole.STAKEHOLDER:
        return True  # Can edit all data
    else:
        return data_owner_id == current_user_id  # Others can only edit their own data
