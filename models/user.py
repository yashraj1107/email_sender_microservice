from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False, nullable=False)

    # OTP fields
    otp_code = Column(String, nullable=True)
    otp_expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    otp_last_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    otp_send_count = Column(Integer, default=0)
    otp_window_start = Column(TIMESTAMP(timezone=True), nullable=True)
    otp_blocked_until = Column(TIMESTAMP(timezone=True), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
