import pytest
from app.palindrome import Palindrome, Language

def test_non_palindrome_english():
    text = "non-palindrome word"
    assert Palindrome(text, Language.EN).is_palindrome() == False

def test_palindrome_english():
    text = "Able was I ere I saw Elba"
    assert Palindrome(text, Language.EN).is_palindrome() == True
    text = \
    """Doc, note
    I
    dissent.A
    fast
    never
    prevents
    a
    fatness.I
    diet
    on
    cod."""
    assert Palindrome(text, Language.EN).is_palindrome() == True

def test_non_palindrome_spanish():
    text = "verbio no es palindrome"
    assert Palindrome(text, Language.ES).is_palindrome() == False
    text = "ñoon"
    assert Palindrome(text, Language.ES).is_palindrome() == False

def test_palindrome_spanish():
    text = "Dábale arroz a la zorra el abad"
    assert Palindrome(text, Language.ES).is_palindrome() == True
    text = "ába"
    assert Palindrome(text, Language.ES).is_palindrome() == True
    text = "    á     b    @#$$%$$%^&* a"
    assert Palindrome(text, Language.ES).is_palindrome() == True
    text = "ñoyoñ"
    assert Palindrome(text, Language.ES).is_palindrome() == True