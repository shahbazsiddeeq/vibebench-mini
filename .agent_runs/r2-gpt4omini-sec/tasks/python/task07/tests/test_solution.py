from src.solution import mask_email


def test_basic():
    assert mask_email("Contact john.doe@example.com") == "Contact j***e@example.com"


def test_short_user():
    assert mask_email("a@x.io") == "a***a@x.io"  # first==last for 1-char usernames


def test_two_char_user():
    assert mask_email("ab@x.io") == "a***b@x.io"


def test_tld_less_address():
    assert mask_email("send to user@localhost now") == "send to u***r@localhost now"


def test_domain_case_preserved():
    assert mask_email("bob@Example.COM") == "b***b@Example.COM"


def test_multiple():
    s = "x@y.com ; jane-doe@sub.domain.org"
    out = mask_email(s)
    assert out == "x***x@y.com ; j***e@sub.domain.org"


def test_non_email_unchanged():
    assert mask_email("no address here, just @ symbols and text") == (
        "no address here, just @ symbols and text"
    )
