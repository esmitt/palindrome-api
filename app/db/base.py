import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import get_settings

load_dotenv()
DATABASE_URL = get_settings().DATABASE_URL


def get_engine():
    settings = get_settings()
    return create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
        echo=settings.DEBUG
    )


def get_base():
    base = declarative_base()
    print(f"get_base returning: {base}")
    return base


def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine, base):
    base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    engine = get_engine()
    SessionLocal = get_session_local(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
