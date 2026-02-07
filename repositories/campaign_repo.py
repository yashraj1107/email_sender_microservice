from sqlalchemy.orm import Session
from models.campagin import Campaign

def create_campaign(
    db: Session,
    user_id: int,
    name: str,
    subject: str,
    body: str
) -> Campaign:
    new_campaign = Campaign(
        name=name,
        subject=subject,
        body=body,
        user_id=user_id,
        status="draft"
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign


def get_campaign_by_id(
    db: Session,
    campaign_id: int,
    user_id: int
) -> Campaign | None:
    return db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == user_id
    ).first()
