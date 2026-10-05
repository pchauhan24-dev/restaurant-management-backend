from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal


class MenuItemCreate(BaseModel):
    name: str
    category: Literal[
        "Starter",
        "Main Course",
        "Dessert",
        "Drinks"
    ]
    price: float
    description: str
    image_url: Optional[HttpUrl] = None
    is_available: bool = True


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[
        Literal[
            "Starter",
            "Main Course",
            "Dessert",
            "Drinks"
        ]
    ] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    is_available: Optional[bool] = None