from pydantic import BaseModel
from datetime import datetime


class ListCreate(BaseModel):
    name: str


class ListOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
