from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import menu_collection, orders_collection
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.utils.dependencies import require_customer, require_admin


router = APIRouter(
    tags=["Orders"]
)


# Customer: Place an order
@router.post("/order")
def create_order(
    order: OrderCreate,
    current_user=Depends(require_customer)
):
    if not order.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item"
        )

    order_items = []
    total_price = 0.0

    for item in order.items:

        # Validate food ID
        try:
            food_object_id = ObjectId(item.food_id)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid food ID: {item.food_id}"
            )

        # Find food item
        food = menu_collection.find_one(
            {"_id": food_object_id}
        )

        if not food:
            raise HTTPException(
                status_code=404,
                detail=f"Food item not found: {item.food_id}"
            )

        # Check availability
        if not food.get("is_available", False):
            raise HTTPException(
                status_code=400,
                detail=f"{food['name']} is currently unavailable"
            )

        item_total = food["price"] * item.quantity
        total_price += item_total

        order_items.append({
            "food_id": item.food_id,
            "name": food["name"],
            "price": food["price"],
            "quantity": item.quantity
        })

    order_data = {
        "user_id": current_user["id"],
        "items": order_items,
        "total_price": total_price,
        "status": "Pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    result = orders_collection.insert_one(order_data)

    return {
        "message": "Order placed successfully",
        "order_id": str(result.inserted_id),
        "total_price": total_price,
        "status": "Pending"
    }


# Customer: View order history
@router.get("/my-orders")
def get_my_orders(
    current_user=Depends(require_customer)
):
    orders = list(
        orders_collection.find(
            {"user_id": current_user["id"]}
        )
    )

    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]

    return orders


# Customer: Cancel an order
@router.put("/order/{order_id}/cancel")
def cancel_order(
    order_id: str,
    current_user=Depends(require_customer)
):
    try:
        object_id = ObjectId(order_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    order = orders_collection.find_one({
        "_id": object_id,
        "user_id": current_user["id"]
    })

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order["status"] != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Order can only be cancelled while it is Pending"
        )

    orders_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": "Cancelled"
            }
        }
    )

    return {
        "message": "Order cancelled successfully",
        "order_id": order_id,
        "status": "Cancelled"
    }


# Admin: View all orders
@router.get("/orders")
def get_all_orders(
    current_user=Depends(require_admin)
):
    orders = list(
        orders_collection.find()
    )

    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]

    return orders


# Admin: Update order status
@router.put("/order/{order_id}/status")
def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    current_user=Depends(require_admin)
):
    # Validate order ID
    try:
        object_id = ObjectId(order_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    # Check order exists
    order = orders_collection.find_one(
        {"_id": object_id}
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Update status
    orders_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": status_data.status
            }
        }
    )

    return {
        "message": "Order status updated successfully",
        "order_id": order_id,
        "status": status_data.status
    }