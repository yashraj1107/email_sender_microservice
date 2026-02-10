from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.session import Base


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
