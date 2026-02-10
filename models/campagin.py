from sqlalchemy import Column, Integer, String, Float, BigInteger,text,TIMESTAMP,Boolean,ForeignKey,UniqueConstraint
from db.session import Base
from sqlalchemy import Enum as SqlEnum
from core.enums import CampaignStatus
from sqlalchemy.orm import relationship

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)

    status = Column(String, nullable=False, server_default="draft")

    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
    )

    user = relationship("User", back_populates="campaigns")
    list = relationship("List")



