from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models.campagin,models.user,schemas.campagin
from db.session import get_db
from core.oauth2 import get_current_user

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
    dependencies=[Depends(get_current_user)]
)

@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.campagin.CampaignOut)
def create_campagin(campaign:schemas.campagin.CampaignCreate,db:Session=Depends(get_db),current_user: models.user.User = Depends(get_current_user)):
    new_campaign=models.campagin.Campaign(name=campaign.name,subject=campaign.subject,body=campaign.body,user_id=current_user.id,status="draft")
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.get("/{campaign_id}",status_code=status.HTTP_200_OK,response_model=schemas.campagin.CampaignOut)
def get_campagin(campaign_id:int,db:Session=Depends(get_db),current_user:models.user.User=Depends(get_current_user)):
    campaign=db.query(models.campagin.Campaign).filter(models.campagin.Campaign.id == campaign_id,models.campagin.Campaign.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=400,detail="Campagin Not Found")
    return campaign

@router.post("/{campaign_id}/schedule",status_code=status.HTTP_200_OK,response_model=schemas.campagin.CampaignOut)
def schedule_campaign(campaign_id:int,db:Session=Depends(get_db),current_user:models.user.User=Depends(get_current_user)):
    campaign=db.query(models.campagin.Campaign).filter(models.campagin.Campaign.id == campaign_id,models.campagin.Campaign.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404,detail="Campagin Not Found")
    if campaign.status != "draft":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Campaign cannot be scheduled from status '{campaign.status}'")
    campaign.status = "scheduled"
    db.commit()
    db.refresh(campaign)
    return campaign