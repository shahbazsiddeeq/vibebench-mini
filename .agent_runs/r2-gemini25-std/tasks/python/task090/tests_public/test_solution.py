from src.solution import guess_mime


def test_json():
    assert guess_mime("data.json") == "application/json"


def test_pdf():
    assert guess_mime("doc.pdf") == "application/pdf"


def test_no_extension():
    assert guess_mime("Makefile") == "application/octet-stream"


def test_double_extension_uses_last():
    assert guess_mime("photo.backup.png") == "image/png"
