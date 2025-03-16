from palindrome import Language
from schemas import BaseModel
from sqlalchemy.sql import func
import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class PalindromeRecord(db.Base):
    __tablename__ = "palindrome"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    language = Column(String, index=True)
    timestamp = Column(DateTime(), server_default=func.now())
    is_palindrome = Column(Boolean, default=False)