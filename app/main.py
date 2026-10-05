from fastapi import FastAPI, Depends

from app.routes.auth import router as auth_router
from app.routes.menu import router as menu_router
from app.routes.orders import router as orders_router
from app.utils.dependencies import get_current_user


app = FastAPI(
    title="Restaurant Management Backend API",
    description="Backend API for restaurant menu management and customer orders",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "Restaurant Management Backend API is running"
    }


@app.get("/test-auth")
def test_auth(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Authentication successful",
        "user": {
            "id": current_user["id"],
            "name": current_user["name"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    }