from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from dependencies.mock_auth import get_current_user, require_view_all_data, require_edit_all_data
from models.roles import UserWithRole, UserRole, can_access_user_data, can_edit_user_data

router = APIRouter(prefix="/data", tags=["data-management"])

# Data models
class DataItem(BaseModel):
    id: int
    title: str
    content: str
    owner_id: str
    created_at: str
    updated_at: str = None

class CreateDataItem(BaseModel):
    title: str
    content: str

class UpdateDataItem(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# In-memory storage (replace with database)
data_items_db = []
next_id = 1

@router.get("/", response_model=List[DataItem])
async def get_user_data(current_user: UserWithRole = Depends(get_current_user)):
    """Get data items - all users' data for admin/stakeholder, own data for others"""
    if current_user.role in [UserRole.ADMIN, UserRole.STAKEHOLDER, UserRole.INTERNAL]:
        # Admin, Stakeholder, and Internal users can see all data
        return data_items_db
    else:
        # Normal users can only see their own data
        user_data = [item for item in data_items_db if item["owner_id"] == current_user.uid]
        return user_data

@router.post("/", response_model=DataItem)
async def create_data_item(
    data: CreateDataItem,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Create a new data item for the current user"""
    global next_id
    from datetime import datetime
    
    new_item = {
        "id": next_id,
        "title": data.title,
        "content": data.content,
        "owner_id": current_user.uid,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    data_items_db.append(new_item)
    next_id += 1
    return new_item

@router.get("/{item_id}", response_model=DataItem)
async def get_data_item(
    item_id: int,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Get a specific data item (role-based access)"""
    item = next((item for item in data_items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data item not found"
        )
    
    # Check if user can access this data
    if not can_access_user_data(current_user.role, item["owner_id"], current_user.uid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this data item"
        )
    
    return item

@router.put("/{item_id}", response_model=DataItem)
async def update_data_item(
    item_id: int,
    data: UpdateDataItem,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Update a data item (role-based access)"""
    item = next((item for item in data_items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data item not found"
        )
    
    # Check if user can edit this data
    if not can_edit_user_data(current_user.role, item["owner_id"], current_user.uid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to edit this data item"
        )
    
    item_index = data_items_db.index(item)
    from datetime import datetime
    if data.title is not None:
        data_items_db[item_index]["title"] = data.title
    if data.content is not None:
        data_items_db[item_index]["content"] = data.content
    
    data_items_db[item_index]["updated_at"] = datetime.now().isoformat()
    return data_items_db[item_index]

@router.delete("/{item_id}")
async def delete_data_item(
    item_id: int,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Delete a data item (role-based access)"""
    item = next((item for item in data_items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data item not found"
        )
    
    # Check if user can edit this data (same as update permission)
    if not can_edit_user_data(current_user.role, item["owner_id"], current_user.uid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to delete this data item"
        )
    
    item_index = data_items_db.index(item)
    deleted_item = data_items_db.pop(item_index)
    return {"message": f"Data item '{deleted_item['title']}' deleted successfully"}

@router.get("/search/{query}")
async def search_data_items(
    query: str,
    current_user: UserWithRole = Depends(get_current_user)
):
    """Search data items by title or content (role-based access)"""
    if current_user.role in [UserRole.ADMIN, UserRole.STAKEHOLDER, UserRole.INTERNAL]:
        # Admin, Stakeholder, and Internal users can search all data
        searchable_items = data_items_db
    else:
        # Normal users can only search their own data
        searchable_items = [item for item in data_items_db if item["owner_id"] == current_user.uid]
    
    matching_items = [
        item for item in searchable_items 
        if query.lower() in item["title"].lower() or query.lower() in item["content"].lower()
    ]
    return matching_items
