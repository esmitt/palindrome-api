from sqlalchemy.sql import func
from db import get_base, get_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

Base = get_base()
engine = get_engine()

# Base.metadata.bind = engine

class PalindromeRecord(Base):
    __tablename__ = "palindrome"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    language = Column(String)
    timestamp = Column(DateTime(), server_default=func.now())
    is_palindrome = Column(Boolean)