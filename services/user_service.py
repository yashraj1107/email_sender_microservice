from repositories import user_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from utils.utils import get_password_hash,verify_password,create_access_token,create_refresh_token
from datetime import timedelta
from jose import JWTError, jwt
from core.config import settings

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
    
    access_token = create_access_token(
    data={"sub": str(existing_user.id)},
    expires_delta=timedelta(minutes=15)
)

def refresh_user_token(refresh_token: str):

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    new_access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=15)
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }