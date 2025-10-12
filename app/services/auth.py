import os
import app.services.utils as utils
import jwt
from jwt.exceptions import InvalidTokenError
import app.services.users as user_services
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated
from ..schemas.user import TokenData
from ..models.user import User
from ..database import get_db

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


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















































# from ..models.user import User, RefreshToken
# from ..schemas.users import UserCreate, UserOut

# import jwt
# import os
# from sqlalchemy import or_
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, Depends
# from passlib.context import CryptContext
# from datetime import datetime, timezone, timedelta
# from dotenv import load_dotenv

# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
# from fastapi.security import OAuth2PasswordBearer
# import secrets
# from pydantic import EmailStr


# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db: Session, identifier: str):
#     return db.query(User).filter(or_(User.username == identifier,User.email == identifier)).first()

# def create_user(db: Session, data: UserCreate):
#     username = db.query(User).filter(User.username == data.username).first()
#     email = db.query(User).filter(User.email == data.email).first()
#     if username:
#         raise HTTPException(status_code=400, detail ="username already exists")
#     if email:
#         raise HTTPException(status_code=400, detail ="email already exists")
#     hashed_password = get_password_hash(data.password)
#     user = User(
#         username = data.username,
#         email = data.email,
#         hashed_password = hashed_password
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return UserOut.model_validate(user)
    
# def authenticate_user(db: Session, identifier:str, password: str):
#     user = get_user(db,identifier)
#     if not user:
#         raise HTTPException(status_code=401, detail="Wrong email or username")
#     if not user.is_verified:
#         raise HTTPException(status_code=401, detail="Account not verified")
#     if not verify_password(password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Wrong password")
#     return user

# def get_current_user(db:Session, token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("id")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid Token")
    
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail = "User not found")
#     return user

# def create_access_token(data:dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
#     return encoded_jwt

# #replace with another secret key
# token_algo = URLSafeTimedSerializer(SECRET_KEY, salt='Email_Verification_&_Forgot_password')

# def token(email: EmailStr):
#     token = token_algo.dumps(email)
#     return token

# def verify_token(db: Session, token:str):
#     try:
#         email = token_algo.loads(token, max_age = 1800)
#     except SignatureExpired:
#         raise HTTPException(status_code=400, detail="Verification token expired")
#     except BadTimeSignature:
#         raise HTTPException(status_code=400, detail="Verification token expired")
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.is_verified = True
#     db.commit()
#     return user

# def create_refresh_token(db: Session, user_id: int, expires_delta: timedelta, device = None, ip = None, remember_me = False):
#     token = secrets.token_urlsafe(32)
#     expires_at = datetime.now(timezone.utc) + expires_delta
#     refresh_token = RefreshToken(
#         user_id = user_id,
#         hashed_token = get_password_hash(token),
#         expires_at = expires_at,
#         remember_me = remember_me,
#         revoked = False,
#         device = device,
#         ip_address = ip
#     )
#     db.add(refresh_token)
#     db.commit()
#     db.refresh(refresh_token)
#     return token

# def validate_refresh_token(db: Session, token: str):
#     refresh_tokens = db.query(RefreshToken).all()
#     for stored_token in refresh_tokens:
#         if verify_password(token, stored_token.hashed_token):
#             if stored_token.revoked or stored_token.expires_at < datetime.now(timezone.utc):
#                 raise HTTPException(status_code=401, detail = "Refresh token invalid")
#             return stored_token
#     raise HTTPException(status_code= 401, detail = "Refresh token not found")


