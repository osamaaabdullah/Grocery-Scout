import app.services.users as user_services

from fastapi import APIRouter, Depends
from ..schemas.user import UserCreate, UserOut, Token
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/user")

@router.post("/signup", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_services.create_user(db, user)

@router.delete("/delete")
async def delete_user(email: str, db: Session = Depends(get_db)):
    return user_services.delete_user(db, email)