import random
from datetime import datetime, timedelta


OTP_EXPIRY_MINUTES = 10
OTP_RESEND_COOLDOWN_SECONDS = 60
OTP_MAX_PER_HOUR = 10
OTP_BLOCK_HOURS = 3


def generate_otp():
    return str(random.randint(100000, 999999))


def get_expiry():
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
