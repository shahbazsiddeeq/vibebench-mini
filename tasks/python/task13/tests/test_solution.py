from src.solution import slugify


def test_accents_and_spaces():
    assert slugify("Crème Brûlée 2025!") == "creme-brulee-2025"


def test_punct_and_trim():
    assert slugify("  Hello,  world --- ") == "hello-world"
