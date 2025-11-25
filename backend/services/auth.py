import os
import backend.services.utils as utils
import jwt
import backend.services.users as user_services
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated
from backend.schemas.user import TokenData, PasswordResetEmail
from backend.models.user import User
from backend.database import get_db
from fastapi_mail import ConnectionConfig, MessageSchema, MessageType

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
VERIFICATION_TOKEN_EXPIRE_MINUTES = int(os.getenv("VERIFICATION_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



def authenticate_user(db: Session, email: str, password:str):
    user = user_services.get_user_by_email(db, email)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user: User, expires_delta: timedelta | None = None):
    to_encode = {
        "sub": user.email,
        "role": user.role
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = user_services.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def role_required(required_role:str):
    async def verify_role(current_user: Annotated[User, Depends(get_current_user)]):
        print(f"Current user: {current_user.email}, role: {current_user.role}")
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Not enough permission")
        return current_user
    return verify_role

def create_verification_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_verification_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except InvalidTokenError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification link."
            )

def get_conf():
    load_dotenv()
    conf = ConnectionConfig(
        MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
        MAIL_FROM = os.getenv("MAIL_FROM"),
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_FROM_NAME="Grocery Scout",
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True
    )
    return conf

def resend_verification_email(db: Session, email:str, verify_link:str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified.")
    
    return get_verification_email_body(email, verify_link)

def get_verification_email_body(email: str, verify_link: str):
    html =  f"""
            <h1>Verify your Grocery Scout Account</h1>
            <p>Please click on this link to verify your account</p>
            <a href="{verify_link}">Activate account</a>
            """
    message = MessageSchema(
        subject="Activate your Grocery Scout Account",
        recipients=[email],
        body = html,
        subtype= MessageType.html
    )
    return message

def authenticate_user_for_verification(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.is_verified=True
    db.commit()
    db.refresh(user)
    return {"message": "Account verified"}

def create_password_reset_token(db: Session, email: PasswordResetEmail):
    user = user_services.get_user_by_email(db, email.email)
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    expire = datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email.email,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password_reset_token(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        email = payload.get("sub")
        return email
    except InvalidTokenError:
        raise HTTPException(status_code=400,
                            detail="Invalid or expired verification link.")
    
def update_password(db: Session, email: str, password: str):
    utils.password_strength(password)
    user = user_services.get_user_by_email(db, email)
    if user:
        user.hashed_password = utils.get_password_hash(password)
        db.commit()
        db.refresh(user)

def get_reset_password_body(email: str, verify_link: str):
    html =  f"""
            <h1>Reset your Grocery Scout Account password</h1>
            <p>Please click on this link to reset your password</p>
            <a href="{verify_link}">Reset Password</a>
            """
    message = MessageSchema(
        subject="Reset your Grocery Scout Account password",
        recipients=[email],
        body = html,
        subtype= MessageType.html
    )
    return message