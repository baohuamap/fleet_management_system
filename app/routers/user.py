from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database import fake_users_db
from app.schemas import Token
from app.security.oauth2 import create_access_token
from app.security.utils import authenticate_user

router = APIRouter(prefix="/token", tags=["USER LOGIN"])


@router.post("/", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(
        user_db=fake_users_db,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
