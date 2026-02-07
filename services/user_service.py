from repositories import user_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.utils import get_password_hash

def register_user(db, email, password):
    existing_user = user_repo.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(...)

    hashed_password = get_password_hash(password)

    return user_repo.create_user(db, email, hashed_password)
