from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.oauth2 import get_current_user
from services import campaign_service
from schemas.campagin import CampaignCreate, CampaignOut
from models.user import User
from schemas.common import APIResponse


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)

@router.post("", status_code=status.HTTP_201_CREATED,  response_model=APIResponse[CampaignOut])
def create_campaign(campaign: CampaignCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    created_campaign = campaign_service.create_campaign(db=db,user_id=current_user.id,name=campaign.name,subject=campaign.subject,body=campaign.body)
    return APIResponse(success=True,message="Campaign created successfully",data=created_campaign)

@router.get("/{campaign_id}", response_model=APIResponse[CampaignOut])
def get_campaign(campaign_id: int,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign=campaign_service.get_campaign(
        db=db,
        campaign_id=campaign_id,
        user_id=current_user.id
    )
    return APIResponse(success=True,message="Campaign fetched successfully",data=campaign)

@router.post("/{campaign_id}/schedule",  response_model=APIResponse[CampaignOut])
def schedule_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign_schedule=campaign_service.schedule_campaign(
        db=db,
        campaign_id=campaign_id,
        user_id=current_user.id
    )
    return APIResponse(success=True,message="Campaign fetched successfully",data=campaign_schedule)
