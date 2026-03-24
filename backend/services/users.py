from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate, UserOut
from backend.core.security import password_strength, get_password_hash
from backend.core.exceptions import UserAlreadyExistsError, UserNotFoundError


def create_user(db: Session, user: UserCreate) -> User:
    if db.query(User).filter(User.email == user.email).first():
        raise UserAlreadyExistsError(user.email)
    hashed_password = get_password_hash(user.password)
    new_user = User(email = user.email, hashed_password = hashed_password, name = user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
    
def delete_user(db: Session, email:str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UserNotFoundError(email)
    db.delete(user)
    db.commit()
    return {
        "message": "Account deleted."
    }