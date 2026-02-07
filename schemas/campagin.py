from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from core.enums import CampaignStatus

class CampaignCreate(BaseModel):
    name:str
    subject:str
    body:str

class CampaignOut(BaseModel):
    id:int
    name:str
    subject:str
    body:str
    status:CampaignStatus
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ContactIn(BaseModel):
    email_id:EmailStr

class ContactOut(BaseModel):
    id:int
    email_id:EmailStr
    created_at: datetime    
    class Config:
        from_attributes = True