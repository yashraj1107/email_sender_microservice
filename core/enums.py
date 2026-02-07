from enum import Enum

class CampaignStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    sent = "sent"
    failed = "failed"
