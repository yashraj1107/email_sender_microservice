from sqlalchemy import Column, Integer, String, Float, BigInteger,text,TIMESTAMP,Boolean,ForeignKey,UniqueConstraint
from db.session import Base
from sqlalchemy import Enum as SqlEnum
from core.enums import CampaignStatus
from sqlalchemy.orm import relationship

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    user = relationship("User", back_populates="lists")
    contacts = relationship("ListContact", back_populates="list", cascade="all, delete")

class ListContact(Base):
    __tablename__ = "list_contacts"

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"))
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint("list_id", "contact_id", name="unique_list_contact"),
    )
    list = relationship("List", back_populates="contacts")
    contact = relationship("Contact", back_populates="lists")