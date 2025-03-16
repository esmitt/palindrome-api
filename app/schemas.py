from pydantic import BaseModel, Field
from palindrome import Language
from datetime import datetime

class PalindromeBase(BaseModel):
    text: str = Field(..., min_length=1, description="Text to check if is palindrome. This will be stored")
    language: Language = Field(default=Language.EN, description="Language of the text (EN, ES)")

class PalindromeSchema(PalindromeBase):
    pass

class PalindromeResponse(BaseModel):
    id: int
    is_palindrome: bool = False
    timestamp: datetime

    class ConfigDict:
        from_attributes = True

class PalindromeQuery(BaseModel):
    id: int
    text: str
    timestamp: datetime
    language: Language
