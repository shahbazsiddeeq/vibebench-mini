from src.solution import guess_mime


def test_html():
    assert guess_mime("index.html") == "text/html"


def test_png():
    assert guess_mime("image.png") == "image/png"


def test_unknown_extension():
    assert guess_mime("file.qzqzqz") == "application/octet-stream"


def test_empty_string():
    assert guess_mime("") == "application/octet-stream"


def test_case_insensitive():
    assert guess_mime("INDEX.HTML") == guess_mime("index.html")
