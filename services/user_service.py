from repositories import user_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from utils.utils import get_password_hash,verify_password,create_access_token

def register_user(db, email, password):
    existing_user = user_repo.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(status_code=400,detail="Email ID already exsits, please login")

    hashed_password = get_password_hash(password)

    return user_repo.create_user(db, email, hashed_password)

def login_user(db,email,password):
    existing_user = user_repo.get_user_by_email(db, email)

    if not existing_user:
        raise HTTPException(status_code=400,detail="Email ID does not exsit")
    
    if not verify_password(password,existing_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect Password")
    
    access=create_access_token(data={"sub": existing_user.id})
    
    return {"access_token":access}