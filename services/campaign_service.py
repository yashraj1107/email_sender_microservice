from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories import campaign_repo
from models.campagin import Campaign
from core.enums import CampaignStatus


def create_campaign(
    db: Session,
    user_id: int,
    name: str,
    subject: str,
    body: str
) -> Campaign:
    return campaign_repo.create_campaign(
        db=db,
        user_id=user_id,
        name=name,
        subject=subject,
        body=body
    )

def get_campaign(
    db: Session,
    campaign_id: int,
    user_id: int
) -> Campaign:
    campaign = campaign_repo.get_campaign_by_id(
        db=db,
        campaign_id=campaign_id,
        user_id=user_id
    )

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    return campaign


def schedule_campaign(
    db: Session,
    campaign_id: int,
    user_id: int
) -> Campaign:
    campaign = get_campaign(db, campaign_id, user_id)

    if campaign.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campaign cannot be scheduled from status '{campaign.status}'"
        )

    campaign.status = CampaignStatus.scheduled
    db.commit()
    db.refresh(campaign)

    return campaign
