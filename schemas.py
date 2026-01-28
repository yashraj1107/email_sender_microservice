from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email_id:EmailStr
    password:str

class UserLogin(BaseModel):
    email_id:EmailStr
    password:str