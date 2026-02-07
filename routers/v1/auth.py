from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.session import get_db
from services import user_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=["users"],
)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(
        db=db,
        email=user.email_id,
        password=user.password
    )

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return user_service.login_user(
        db=db,
        email=form_data.username, 
        password=form_data.password
    )

@router.post("/refresh")
def refresh_token(refresh_token: str):
    return user_service.refresh_user_token(refresh_token)

