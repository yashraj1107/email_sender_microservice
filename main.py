from fastapi import FastAPI,status,HTTPException,Depends
from database import SessionLocal, engine
import models,schemas,database
from sqlalchemy.orm import Session
from utils import get_password_hash,verify_password,create_access_token
from dotenv import load_dotenv
import os

models.Base.metadata.create_all(bind=engine)


load_dotenv()
app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@app.get("/")
def root():
    return{"hello world"}

@app.post("/register",status_code=status.HTTP_201_CREATED)
def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(models.User).filter_by(email=user.email_id).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hash_password=get_password_hash(user.password)
    new_user=models.User(email_id=user.email_id,password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message":"user created"}

@app.post("/login",status_code=status.HTTP_200_OK)
def login(user:schemas.UserLogin,db:Session=Depends(get_db)):
    user_db=db.query(models.User).filter_by(email=user.email_id).first()
    if not user_db:
        raise HTTPException(status_code=400,detail="Email ID does not exsit")
    hash_pass=user_db.password
    if not verify_password(user.password,hash_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect Password")
    access=create_access_token(data={"sub": user_db.id})
    return{"access_token":access}