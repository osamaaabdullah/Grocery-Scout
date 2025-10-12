from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserOut
from fastapi import HTTPException
from app.services.utils import get_password_hash


def create_user(db: Session, user: UserCreate) ->UserOut:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    hashed_password = get_password_hash(user.password)
    user = User(email = user.email, hashed_password = hashed_password, is_active = True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
    
def delete_user(db: Session, email:str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail= 'User not found'
        )
    db.delete(user)
    db.commit()
    return {
        "message": "Account deleted."
    }