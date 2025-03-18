from pydantic import BaseModel, Field
from language import Language
from datetime import datetime

class PalindromeBase(BaseModel):
    text: str = Field(..., min_length=1, description="Text to check if is palindrome. This will be stored")
    language: Language = Field(default=Language.EN, description="Language of the text (EN, ES)")

class PalindromeSchema(PalindromeBase):
    pass

class PalindromeId(BaseModel):
    id: int
    timestamp: datetime
    language: Language

class PalindromeResponse(PalindromeId):
    is_palindrome: bool = False
    model_config = {
        "from_attributes": True
    }

class PalindromeQuery(PalindromeId):
    text: str

class PalindromeQueryById(PalindromeQuery):
    is_palindrome: bool = False

class DeleteResponse(BaseModel):
    success: bool
    message: str