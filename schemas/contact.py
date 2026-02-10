from pydantic import BaseModel, EmailStr
from datetime import datetime


class ContactCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class ContactOut(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
