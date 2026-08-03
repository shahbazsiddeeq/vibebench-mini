from src.solution import mask_email


def test_basic():
    assert mask_email("Contact john.doe@example.com") == "Contact j***e@example.com"


def test_two_char_user():
    assert mask_email("ab@x.io") == "a***b@x.io"


def test_domain_case_preserved():
    assert mask_email("bob@Example.COM") == "b***b@Example.COM"


def test_non_email_unchanged():
    assert mask_email("no address here, just @ symbols and text") == (
        "no address here, just @ symbols and text"
    )
