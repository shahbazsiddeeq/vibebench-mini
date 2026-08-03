import pytest
from src.solution import classify_status


def test_informational():
    assert classify_status(100) == "informational"


def test_redirect():
    assert classify_status(301) == "redirect"


def test_server_error():
    assert classify_status(500) == "server_error"


def test_below_range_raises():
    with pytest.raises(ValueError):
        classify_status(99)


@pytest.mark.parametrize(
    "code,expected",
    [
        (100, "informational"),
        (199, "informational"),
        (200, "success"),
        (299, "success"),
        (300, "redirect"),
        (399, "redirect"),
        (400, "client_error"),
        (499, "client_error"),
        (500, "server_error"),
        (599, "server_error"),
    ],
)
def test_class_boundaries(code, expected):
    assert classify_status(code) == expected
