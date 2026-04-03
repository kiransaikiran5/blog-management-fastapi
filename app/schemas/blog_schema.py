from pydantic import BaseModel, field_serializer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

class BlogCreate(BaseModel):
    title: str
    content: str
    status: str

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
            
    # ✅ AUTO timezone conversion (BEST PRACTICE)
    @field_serializer("created_at", "updated_at", mode="plain")
    def convert_datetime(self, value: datetime) -> str:
        if value is None:
            return None

        # 🔥 Fix naive datetime (SQLite issue)
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        # ✅ Convert UTC → IST
        value = value.astimezone(IST)

        # ✅ Return formatted time
        return value.strftime("%Y-%m-%d %H:%M:%S")