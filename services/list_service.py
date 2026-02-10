from sqlalchemy.orm import Session
from models.list import List

def create_list(db: Session, user_id: int, name: str):
    new_list = List(user_id=user_id, name=name)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list
