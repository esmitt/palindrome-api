from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.base import get_base, get_engine

Base = get_base()
engine = get_engine()


class PalindromeRecord(Base):
    __tablename__ = "palindrome"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    language = Column(String)
    timestamp = Column(DateTime(), server_default=func.now())
    is_palindrome = Column(Boolean)
