import backend.services.users as user_services
import backend.services.auth as auth_services
from fastapi import APIRouter, Depends
from backend.schemas.user import UserCreate, UserOut, PasswordReset, PasswordResetEmail
from backend.dependencies.db import get_read_db, get_write_db
from sqlalchemy.orm import Session

from backend.core.config import get_settings


router = APIRouter(prefix="/user", tags = ["Users"])
settings = get_settings()

@router.post("/signup", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_write_db)):
    new_user = user_services.create_user(db, user)
    await auth_services.send_verification(db, new_user.email)
    return new_user


@router.get("/verify/{token}")
async def verify_user(token: str, db: Session = Depends(get_write_db)):
    return auth_services.authenticate_user_for_verification(db, token)


@router.post("/resend")
async def resend_verification(email: str, db: Session = Depends(get_read_db)):
    await auth_services.resend_verification_email(db, email)
    return {"message": "Verification email has been sent."}


@router.post("/forgot-password")
async def forgot_password(body: PasswordResetEmail, db: Session = Depends(get_read_db)):
    await auth_services.send_password_reset(db, body.email)
    return {"message": "Password reset link has been sent."}


@router.post("/reset-password/{token}")
async def reset_password(token: str, password: PasswordReset, db: Session = Depends(get_write_db)):
    auth_services.reset_password(db, token, password.password)
    return {"message": "Password has been reset"}