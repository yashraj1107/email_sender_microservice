from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas.user
from schemas.user import UserCreate
from db.session import get_db
from core.oauth2 import get_current_user
from services import user_service

router = APIRouter(
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(
        db=db,
        email=user.email_id,
        password=user.password
    )

@router.post("/login",status_code=status.HTTP_200_OK)
def login(user:schemas.user.UserLogin,db:Session=Depends(get_db)):
    return user_service.login_user(
        db=db,
        email=user.email_id,
        password=user.password
    )
