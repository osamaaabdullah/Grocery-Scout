from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.user import Token
from sqlalchemy.orm import Session
from backend.database import get_db
import backend.services.auth as auth_services 

router = APIRouter(prefix="/auth", tags = ["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = auth_services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "Incorrect email or password",
                            headers= {"WWW-Authenticate": "Bearer"})
    access_token = auth_services.create_access_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }