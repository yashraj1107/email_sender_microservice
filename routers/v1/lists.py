from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.oauth2 import get_current_user
from models.user import User
from schemas.list import ListCreate, ListOut
from services import list_service

router = APIRouter(prefix="/lists", tags=["Lists"])


@router.post("", response_model=ListOut)
def create_list(
    list_data: ListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_service.create_list(
        db=db,
        user_id=current_user.id,
        name=list_data.name,
    )
