from sqlalchemy.orm import Session
from models.list_contact import Contact
from models.list_contact import ListContact

def create_contact(db: Session, user_id: int, first_name, last_name, email):
    contact = Contact(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def add_contact_to_list(db: Session, list_id: int, contact_id: int):
    mapping = ListContact(list_id=list_id, contact_id=contact_id)
    db.add(mapping)
    db.commit()
    return mapping