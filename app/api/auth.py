from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.api import deps
from app.api.deps import get_current_active_user
from app.core.config import settings
from app.domain.user import User
from app.service.auth import (
    Token,
    authenticate_user,
    create_access_token,
    create_user,
    SignUpIn,
    MeOut,
)
from app.utils import CustomJSONResponse

router = APIRouter()


@router.post("/signup", response_class=CustomJSONResponse)
def signup(signup_in: SignUpIn, session: Session = Depends(dependency=deps.get_db)):
    create_user(signup_in, session)
    return


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(dependency=deps.get_db),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=MeOut)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
