from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models.user,schemas.user
from db.session import get_db
from core.oauth2 import get_current_user
from utils.utils import get_password_hash,verify_password,create_access_token
router = APIRouter(
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user:schemas.user.UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(models.user.User).filter_by(email=user.email_id).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hash_password=get_password_hash(user.password)
    new_user=models.user.User(email_id=user.email_id,password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message":"user created"}

@router.post("/login",status_code=status.HTTP_200_OK)
def login(user:schemas.user.UserLogin,db:Session=Depends(get_db)):
    user_db=db.query(models.user.User).filter_by(email=user.email_id).first()
    if not user_db:
        raise HTTPException(status_code=400,detail="Email ID does not exsit")
    hash_pass=user_db.password
    if not verify_password(user.password,hash_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect Password")
    access=create_access_token(data={"sub": user_db.id})
    return{"access_token":access}
