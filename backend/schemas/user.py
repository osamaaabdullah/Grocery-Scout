from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    provider: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    user_id: int
    name: str
    role: str
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    model_config = ConfigDict(from_attributes = True)
        

class OAuthAccountBase(BaseModel):
    provider: str
    provider_account_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    
class OAuthAccountCreate(OAuthAccountBase):
    pass

class OAuthAccount(OAuthAccountBase):
    id: int
    
    model_config = ConfigDict(from_attributes = True)
        
class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetEmail(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    password: str