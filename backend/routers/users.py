import backend.services.users as user_services
import backend.services.auth as auth_services
from fastapi import APIRouter, Depends
from backend.schemas.user import UserCreate, Token, PasswordReset, PasswordResetEmail
from backend.database import get_read_db, get_write_db
from sqlalchemy.orm import Session
from fastapi_mail import FastMail
from dotenv import load_dotenv
import os
router = APIRouter(prefix="/user", tags = ["Users"])


@router.post("/signup")
async def create_user(user: UserCreate, db: Session = Depends(get_write_db)):
    load_dotenv()
    website_url = os.getenv("WEBSITE_URL")
    created_user = user_services.create_user(db, user)
    token = auth_services.create_verification_token(created_user.email)
    verify_link = f"{website_url}/verify/{token}"
    email_body = auth_services.get_verification_email_body(created_user.email, verify_link)
    fm = FastMail(auth_services.get_conf())
    await fm.send_message(email_body)
    return {"message": "Verification email has been sent."}

@router.get("/verify/{token}")
async def verify_user(token:str, db: Session = Depends(get_read_db)):
    email = auth_services.verify_verification_token(token)
    return auth_services.authenticate_user_for_verification(db,email)

@router.get("/resend")
async def resend_verification_email(email:str, db: Session = Depends(get_read_db)):
    load_dotenv()
    website_url = os.getenv("WEBSITE_URL")
    token = auth_services.create_verification_token(email)
    verify_link = f"{website_url}/verify/{token}"
    email_body = auth_services.resend_verification_email(db, email, verify_link)
    fm = FastMail(auth_services.get_conf())
    await fm.send_message(email_body)
    return {"message": "Verification email has been sent."}

@router.post("/forgot-password")
async def forgot_password(email: PasswordResetEmail, db: Session = Depends(get_write_db)):
    load_dotenv()
    website_url = os.getenv("WEBSITE_URL")
    token = auth_services.create_password_reset_token(db, email)
    verify_link = f"{website_url}/reset-password/{token}"
    email_body = auth_services.get_reset_password_body(email.email, verify_link)
    fm = FastMail(auth_services.get_conf())
    await fm.send_message(email_body)
    return {"message": "Password reset link has been sent."}

@router.post("/reset-password/{token}")
async def reset_password(token:str, password: PasswordReset, db: Session = Depends(get_write_db)):
    email = auth_services.verify_password_reset_token(token)
    auth_services.update_password(db, email, password.password)
    return {"message": "Password has been reset"}

#implement user only delete
# @router.delete("/delete")
# async def delete_user(email: str, db: Session = Depends(get_db)):
#     return user_services.delete_user(db, email)