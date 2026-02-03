from fastapi import FastAPI,status,HTTPException,Depends
from database import SessionLocal, engine
import models,schemas,database
from sqlalchemy.orm import Session
from utils import get_password_hash,verify_password,create_access_token
from dotenv import load_dotenv
import os
from oauth2 import get_current_user

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


@app.post("/campaign",status_code=status.HTTP_201_CREATED)
def create_campagin(campaign:schemas.CampaignCreate,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):
    new_campaign=models.Campaign(name=campaign.name,subject=campaign.subject,body=campaign.body,user_id=current_user.id,status="draft")
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return{"message":"Campaign Created Successfully"}


@app.get("/campaign/{campaign_id}",status_code=status.HTTP_200_OK,response_model=schemas.CampaignOut)
def get_campagin(campaign_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    campaign=db.query(models.Campaign).filter(models.Campaign.id == campaign_id,models.Campaign.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=400,detail="Campagin Not Found")
    return campaign

@app.post("/campaign/{campaign_id}/schedule",status_code=status.HTTP_200_OK)
def schedule_campaign(campaign_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    campaign=db.query(models.Campaign).filter(models.Campaign.id == campaign_id,models.Campaign.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=400,detail="Campagin Not Found")
    if campaign.status != "draft":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Campaign cannot be scheduled from status '{campaign.status}'")
    campaign.status = "scheduled"
    db.commit()
    db.refresh(campaign)
    return campaign

