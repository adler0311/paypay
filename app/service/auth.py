from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class SignUpIn(BaseModel):
    username: str
    password: str
    email: str


class MeOut(BaseModel):
    username: str
    email: str


def get_user(session: Session, username: str):
    return session.scalar(select(User).where(User.username == username))


def authenticate_user(session: Session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_user(signup_in: SignUpIn, session: Session):
    user = User(
        username=signup_in.username,
        email=signup_in.email,
        hashed_password=pwd_context.hash(signup_in.password),
        disabled=False,
    )
    session.add(user)
    session.commit()
