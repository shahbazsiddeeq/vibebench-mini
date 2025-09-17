from src.solution import mask_email

def test_basic():
    assert mask_email("Contact john.doe@example.com") == "Contact j***e@example.com"

def test_short_user():
    assert mask_email("a@x.io") == "a***a@x.io"  # first==last for 1-char usernames

def test_multiple():
    s = "x@y.com ; jane-doe@sub.domain.org"
    out = mask_email(s)
    assert "x***x@y.com" in out and "j***e@sub.domain.org" in out