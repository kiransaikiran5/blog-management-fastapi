from pydantic import BaseModel
from datetime import datetime


# ➕ CREATE COMMENT REQUEST
class CommentCreate(BaseModel):
    content: str
    blog_id: int


# ✅ RESPONSE (VERY IMPORTANT)
class CommentResponse(BaseModel):
    id: int
    content: str
    blog_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True