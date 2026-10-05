from pydantic import BaseModel, Field
from typing import List, Literal


class OrderItemCreate(BaseModel):
    food_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: Literal[
        "Pending",
        "Preparing",
        "Out for delivery",
        "Delivered",
        "Cancelled"
    ]