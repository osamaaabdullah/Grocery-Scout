from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.user import Token
from sqlalchemy.orm import Session
from backend.dependencies.db import get_write_db
import backend.services.auth as auth_service
from backend.core.security import create_access_token
from backend.core.exceptions import UnverifiedUserError

router = APIRouter(prefix="/auth", tags = ["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_write_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user.is_verified:
        raise UnverifiedUserError()
    access_token = create_access_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }