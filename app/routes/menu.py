import re

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import menu_collection
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


# Admin: Add food item
@router.post("/")
def create_menu_item(
    item: MenuItemCreate,
    current_user=Depends(require_admin)
):
    item_data = {
        "name": item.name,
        "category": item.category,
        "price": item.price,
        "description": item.description,
        "image_url": str(item.image_url) if item.image_url else None,
        "is_available": item.is_available
    }

    result = menu_collection.insert_one(item_data)

    return {
        "message": "Food item added successfully",
        "menu_id": str(result.inserted_id)
    }


# Public: View / Search / Filter menu
@router.get("/")
def get_menu(
    search: str | None = Query(
        default=None,
        description="Search by food name or description"
    ),
    category: str | None = Query(
        default=None,
        description="Filter by category"
    )
):
    query = {}

    # Search food name or description
    if search:
        search_regex = {
            "$regex": re.escape(search),
            "$options": "i"
        }

        query["$or"] = [
            {"name": search_regex},
            {"description": search_regex}
        ]

    # Filter by category
    if category:
        query["category"] = category

    menu_items = list(
        menu_collection.find(query)
    )

    for item in menu_items:
        item["id"] = str(item["_id"])
        del item["_id"]

    return menu_items


# Public: View one food item
@router.get("/{menu_id}")
def get_menu_item(menu_id: str):
    try:
        object_id = ObjectId(menu_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid menu item ID"
        )

    item = menu_collection.find_one(
        {"_id": object_id}
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    item["id"] = str(item["_id"])
    del item["_id"]

    return item


# Admin: Update food item
@router.put("/{menu_id}")
def update_menu_item(
    menu_id: str,
    item: MenuItemUpdate,
    current_user=Depends(require_admin)
):
    try:
        object_id = ObjectId(menu_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid menu item ID"
        )

    existing_item = menu_collection.find_one(
        {"_id": object_id}
    )

    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    update_data = {
        key: (
            str(value)
            if key == "image_url" and value is not None
            else value
        )
        for key, value in item.model_dump().items()
        if value is not None
    }

    if update_data:
        menu_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

    return {
        "message": "Food item updated successfully"
    }


# Admin: Delete food item
@router.delete("/{menu_id}")
def delete_menu_item(
    menu_id: str,
    current_user=Depends(require_admin)
):
    try:
        object_id = ObjectId(menu_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid menu item ID"
        )

    result = menu_collection.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    return {
        "message": "Food item deleted successfully"
    }