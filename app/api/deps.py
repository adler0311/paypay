from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
