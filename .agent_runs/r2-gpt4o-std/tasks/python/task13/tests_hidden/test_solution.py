from src.solution import slugify


def test_accents_and_spaces():
    assert slugify("Crème Brûlée 2025!") == "creme-brulee-2025"


def test_empty():
    assert slugify("") == ""


def test_only_punctuation():
    assert slugify("!!! ??? ...") == ""
