from pydantic import BaseModel, EmailStr
from typing import Literal


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["customer", "admin"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str