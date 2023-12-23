from sqlalchemy import Column, String, Integer

from app.domain import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False)
    hashed_password = Column(String(length=100), nullable=False)
