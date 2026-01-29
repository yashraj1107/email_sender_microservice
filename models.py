from sqlalchemy import Column, Integer, String, Float, BigInteger,text,TIMESTAMP,Boolean,ForeignKey
from database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,nullable=False, primary_key=True)
    email_id=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Campaign(Base):
    __tablename__='campaigns'
    id=Column(Integer,nullable=False, primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    name=Column(String,nullable=False)
    subject=Column(String,nullable=False)   
    body=Column(String,nullable=False)
    status = Column(String, nullable=False, server_default="draft")
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),onupdate=text('now()'))

class Contact(Base):
    __tablename__='contacts'
    id=Column(Integer,nullable=False, primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    email_id=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))