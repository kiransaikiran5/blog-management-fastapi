from pydantic import BaseModel, EmailStr
from datetime import datetime


# ➕ REGISTER REQUEST
class UserCreate(BaseModel):
    username: str
    email: EmailStr   # ✅ validates email automatically
    password: str


# 🔐 LOGIN REQUEST (optional)
class UserLogin(BaseModel):
    username: str
    password: str


# ✅ RESPONSE (VERY IMPORTANT)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True