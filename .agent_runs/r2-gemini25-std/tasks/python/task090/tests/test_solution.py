from src.solution import guess_mime


def test_html():
    assert guess_mime("index.html") == "text/html"


def test_json():
    assert guess_mime("data.json") == "application/json"


def test_png():
    assert guess_mime("image.png") == "image/png"


def test_pdf():
    assert guess_mime("doc.pdf") == "application/pdf"


def test_unknown_extension():
    assert guess_mime("file.qzqzqz") == "application/octet-stream"


def test_no_extension():
    assert guess_mime("Makefile") == "application/octet-stream"


def test_empty_string():
    assert guess_mime("") == "application/octet-stream"


def test_double_extension_uses_last():
    assert guess_mime("photo.backup.png") == "image/png"


def test_case_insensitive():
    assert guess_mime("INDEX.HTML") == guess_mime("index.html")
