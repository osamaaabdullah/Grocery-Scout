from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from backend.models.user import User
import backend.services.users as user_services
from backend.dependencies.db import get_read_db
from backend.core.security import decode_access_token
from backend.core.exceptions import AppInvalidTokenError, InsufficientPermissionsError, InactiveUserError, TokenExpiredError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_read_db)]) -> User:
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
    except (AppInvalidTokenError, TokenExpiredError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = user_services.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise InactiveUserError()
    return current_user

def role_required(required_role:str):
    async def verify_role(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role != required_role:
            raise InsufficientPermissionsError()
        return current_user
    return verify_role

