from src.solution import slugify


def test_accents_and_spaces():
    assert slugify("Crème Brûlée 2025!") == "creme-brulee-2025"


def test_punct_and_trim():
    assert slugify("  Hello,  world --- ") == "hello-world"


def test_empty():
    assert slugify("") == ""


def test_underscores():
    assert slugify("hello_world_2025") == "hello-world-2025"


def test_only_punctuation():
    assert slugify("!!! ??? ...") == ""


def test_non_latin_dropped():
    # non-Latin script has no ASCII form, so it slugs to nothing
    assert slugify("日本語") == ""
    assert slugify("日本語 test 123") == "test-123"
