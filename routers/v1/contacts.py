from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.oauth2 import get_current_user
from models.user import User
from schemas.contact import ContactCreate, ContactOut
from services import contact_service

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("", response_model=ContactOut)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return contact_service.create_contact(
        db=db,
        user_id=current_user.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
    )
