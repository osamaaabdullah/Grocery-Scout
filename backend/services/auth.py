from sqlalchemy.orm import Session
from backend.core.security import verify_password, get_password_hash, decode_verification_token, decode_password_reset_token, create_verification_token
from backend.core.exceptions import InvalidCredentialsError, UserNotFoundError, AlreadyVerifiedError
from backend.models.user import User
import backend.services.users as user_services
from backend.services.email import send_verification_email, send_password_reset_email
from backend.core.config import get_settings

settings = get_settings()

def authenticate_user(db: Session, email: str, password:str) -> User:
    user = user_services.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()
    return user

def authenticate_user_for_verification(db: Session, token: str) -> dict:
    email = decode_verification_token(token)
    user = user_services.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(email)
    if user.is_verified:
        raise AlreadyVerifiedError()
    user.is_verified=True
    db.commit()
    db.refresh(user)
    return {"message": "Account verified"}

async def send_verification(db: Session, email: str) -> None:
    user = user_services.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(email)
    token = create_verification_token(email)
    verify_link = f"{settings.website_url}/verify/{token}"
    await send_verification_email(email, verify_link)

async def send_password_reset(db: Session, email: str) -> None:
    from backend.core.security import create_password_reset_token
    user = user_services.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(email)
    token = create_password_reset_token(email)
    reset_link = f"{settings.website_url}/reset-password/{token}"
    await send_password_reset_email(email, reset_link)

async def resend_verification_email(db: Session, email: str) -> None:
    user = user_services.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(email)
    if user.is_verified:
        raise AlreadyVerifiedError()
    token = create_verification_token(email)
    verify_link = f"{settings.website_url}/verify/{token}"
    await send_verification_email(email, verify_link)
    
def reset_password(db: Session, token: str, password: str) -> dict:
    email = decode_password_reset_token(token)
    user = user_services.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(email)
    user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return {"message": "Password reset successful"}

