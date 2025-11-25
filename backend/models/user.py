from backend.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable = False)
    hashed_password = Column(String, nullable=True)
    is_verified = Column(Boolean, nullable=False, default= False)
    is_active = Column(Boolean, nullable=False, default=False)
    provider = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    role = Column(String, nullable=False, default="user")
    oauth_accounts = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    provider = Column(String, nullable=False)
    provider_account_id = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    
    user = relationship("User", back_populates="oauth_accounts")