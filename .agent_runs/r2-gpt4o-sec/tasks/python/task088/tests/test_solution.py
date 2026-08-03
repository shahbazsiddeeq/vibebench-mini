from src.solution import parse_email_headers


def test_basic():
    raw = "From: alice@x.com\nTo: bob@x.com"
    result = parse_email_headers(raw)
    assert result["From"] == "alice@x.com"
    assert result["To"] == "bob@x.com"


def test_folded_header():
    raw = "Subject: Hello\n world"
    result = parse_email_headers(raw)
    # exact unfolded value: a version that drops continuation lines fails here
    assert result["Subject"] == "Hello world"


def test_folded_header_with_tab():
    raw = "Subject: Hello\n\tworld"
    result = parse_email_headers(raw)
    assert result["Subject"] == "Hello world"


def test_multiline_fold():
    raw = "X-Long: a\n b\n c"
    result = parse_email_headers(raw)
    assert result["X-Long"] == "a b c"


def test_duplicate_header_last_wins():
    raw = "X-Test: first\nX-Test: second"
    result = parse_email_headers(raw)
    assert result["X-Test"] == "second"


def test_empty():
    assert parse_email_headers("") == {}


def test_case_normalized():
    result = parse_email_headers("content-type: text/html")
    assert "Content-Type" in result


def test_stops_at_blank_line():
    raw = "From: a\n\nBody text here"
    result = parse_email_headers(raw)
    assert "From" in result
    assert len(result) == 1
