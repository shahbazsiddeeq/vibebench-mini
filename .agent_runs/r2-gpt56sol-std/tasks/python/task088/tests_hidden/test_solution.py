from src.solution import parse_email_headers


def test_basic():
    raw = "From: alice@x.com\nTo: bob@x.com"
    result = parse_email_headers(raw)
    assert result["From"] == "alice@x.com"
    assert result["To"] == "bob@x.com"


def test_folded_header_with_tab():
    raw = "Subject: Hello\n\tworld"
    result = parse_email_headers(raw)
    assert result["Subject"] == "Hello world"


def test_duplicate_header_last_wins():
    raw = "X-Test: first\nX-Test: second"
    result = parse_email_headers(raw)
    assert result["X-Test"] == "second"


def test_case_normalized():
    result = parse_email_headers("content-type: text/html")
    assert "Content-Type" in result
