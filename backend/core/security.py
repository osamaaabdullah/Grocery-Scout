import re
from pwdlib import PasswordHash
from backend.core.exceptions import WeakPasswordError
from backend.core.config import get_settings
import jwt
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError
from datetime import datetime, timedelta, timezone
from backend.core.exceptions import TokenExpiredError, AppInvalidTokenError


settings = get_settings()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes
VERIFICATION_TOKEN_EXPIRE_MINUTES = settings.verification_token_expire_minutes

_password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    password_strength(password)
    return _password_hash.hash(password)

def password_strength(password: str):
    errors = []
    
    if len(password)<8:
        errors.append("Password length must be at least 8 characters.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least 1 digit.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase character.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase character.")
    if not re.search(r"[~`!@#$%^&*()_+=\[\]{};:'\",.<>?/\\|-]", password):
        errors.append("Password must contain at least one special character.")
    if errors:
        raise WeakPasswordError(errors)


def create_access_token(user) -> str:
    to_encode = {
        "sub": user.email,
        "role": user.role,
        "type": "access"
    }
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_verification_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "verify"
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_password_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "password_reset"
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise AppInvalidTokenError()
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTInvalidTokenError:
        raise AppInvalidTokenError()

def decode_access_token(token: str) -> dict:
    return decode_token(token, "access")

def decode_verification_token(token: str) -> str:
    return decode_token(token, "verify")["sub"]

def decode_password_reset_token(token: str) -> str:
    return decode_token(token, "password_reset")["sub"]
