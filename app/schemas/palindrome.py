from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.enums import Language


class PalindromeBase(BaseModel):
    text: str = Field(..., min_length=1, description="Text to check if is palindrome. This will be stored")
    language: Language = Field(default=Language.EN, description="Language of the text (EN, ES)")


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


class PalindromeFull(PalindromeId):
    text: str
    is_palindrome: bool = False


# class PalindromeSchema(PalindromeBase):
#     pass

class DeleteResponse(BaseModel):
    success: bool
    message: str
