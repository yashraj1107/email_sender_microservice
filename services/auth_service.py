from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import user_repo
from utils.utils import get_password_hash, verify_password
from utils.otp import (
    generate_otp,
    get_expiry,
    OTP_RESEND_COOLDOWN_SECONDS,
    OTP_MAX_PER_HOUR,
    OTP_BLOCK_HOURS
)
from utils.utils import create_access_token, create_refresh_token


def register(db: Session, email: str, password: str):
    existing_user = user_repo.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(password)
    user = user_repo.create_user(db, email, hashed_password)

    send_otp_logic(db, user)

    return {"message": "User registered. Verify OTP."}

def send_otp_logic(db: Session, user):
    now = datetime.utcnow()

    # Check block
    if user.otp_blocked_until and user.otp_blocked_until > now:
        raise HTTPException(
            status_code=429,
            detail="Too many OTP attempts. Try later."
        )

    # Cooldown check (1 min)
    if user.otp_last_sent_at and \
       (now - user.otp_last_sent_at).total_seconds() < OTP_RESEND_COOLDOWN_SECONDS:
        raise HTTPException(
            status_code=429,
            detail="OTP recently sent. Please wait."
        )

    # Hour window reset
    if not user.otp_window_start or (now - user.otp_window_start) > timedelta(hours=1):
        user.otp_window_start = now
        user.otp_send_count = 0

    # Check max per hour
    if user.otp_send_count >= OTP_MAX_PER_HOUR:
        user.otp_blocked_until = now + timedelta(hours=OTP_BLOCK_HOURS)
        db.commit()
        raise HTTPException(
            status_code=429,
            detail="Too many OTP requests. Try after some time."
        )

    # Generate OTP
    otp = generate_otp()

    user.otp_code = otp
    user.otp_expires_at = get_expiry()
    user.otp_last_sent_at = now
    user.otp_send_count += 1

    db.commit()

    # TODO: send email here
    print(f"OTP for {user.email}: {otp}")

def verify_otp(db: Session, email: str, otp: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Already verified")

    if user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None

    db.commit()

    return {"message": "Account verified successfully"}

def login(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }
