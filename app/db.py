from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../default.db")

def get_engine():
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )
def get_base():
    base = declarative_base()
    print(f"get_base returning: {base}")
    return base

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(engine, base):
    base.metadata.create_all(bind=engine)