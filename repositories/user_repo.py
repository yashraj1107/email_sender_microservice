from sqlalchemy.orm import Session
from models.user import User

def get_user_by_email(db, email):
    return db.query(User).filter(User.email_id == email).first()

def create_user(db, email, hashed_password):
    user = User(email_id=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user