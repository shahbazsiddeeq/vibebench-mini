from src.solution import mask_email


def test_short_user():
    assert mask_email("a@x.io") == "a***a@x.io"  # first==last for 1-char usernames


def test_tld_less_address():
    assert mask_email("send to user@localhost now") == "send to u***r@localhost now"


def test_multiple():
    s = "x@y.com ; jane-doe@sub.domain.org"
    out = mask_email(s)
    assert out == "x***x@y.com ; j***e@sub.domain.org"
