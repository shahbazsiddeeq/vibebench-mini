from src.solution import slugify


def test_punct_and_trim():
    assert slugify("  Hello,  world --- ") == "hello-world"


def test_underscores():
    assert slugify("hello_world_2025") == "hello-world-2025"


def test_non_latin_dropped():
    # non-Latin script has no ASCII form, so it slugs to nothing
    assert slugify("日本語") == ""
    assert slugify("日本語 test 123") == "test-123"
