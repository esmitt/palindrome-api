import string
import unicodedata
from enum import Enum

class Language(Enum):
    EN = "en"
    ES = "es"

class Palindrome:

    def __init__(self, text: str, language: Language):
        self.text: str = text
        self.language: Language = language
        self.punctuations: set[str] = set(string.punctuation + string.whitespace)

    def is_palindrome(self) -> bool:
        # 1) classic version:
        # cleaned_text = ''.join(char.lower() for char in self.text if char.isalnum())
        # return cleaned_text == cleaned_text[::-1]
        # 2) two pointers approach to pass only once per letter
        left, right = 0, len(self.text) - 1
        while left < right:
            # skip blank spaces, \n\r and punctuations
            while left < right and (self.text[left] in self.punctuations):
                left += 1

            while left < right and (self.text[right] in self.punctuations):
                right -= 1

            left_char = self.text[left].lower()
            right_char = self.text[right].lower()

            # replace accents with non-accent vowels
            if self.language == Language.ES:
                if left_char in "áéíóú":
                    left_char = unicodedata.normalize('NFD', left_char)[0]
                if right_char in "áéíóú":
                    right_char = unicodedata.normalize('NFD', right_char)[0]

            if left_char != right_char:
                return False

            left += 1
            right -= 1
        return True
