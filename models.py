from sqlalchemy import Column, Integer, String, Float, BigInteger
from db import Base


class User(Base):
    __tablename__='users'
    id=Column(Integer,nullable=False, primary_key=True)
    email_id=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
