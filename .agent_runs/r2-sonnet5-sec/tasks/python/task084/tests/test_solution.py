import pytest
from src.solution import classify_status


def test_informational():
    assert classify_status(100) == "informational"


def test_success():
    assert classify_status(200) == "success"


def test_redirect():
    assert classify_status(301) == "redirect"


def test_client_error():
    assert classify_status(404) == "client_error"


def test_server_error():
    assert classify_status(500) == "server_error"


def test_unknown_raises():
    with pytest.raises(ValueError):
        classify_status(999)


def test_below_range_raises():
    with pytest.raises(ValueError):
        classify_status(99)


@pytest.mark.parametrize(
    "code,expected",
    [
        (201, "success"),
        (302, "redirect"),
        (403, "client_error"),
        (503, "server_error"),
    ],
)
def test_parametrized(code, expected):
    assert classify_status(code) == expected


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


@pytest.mark.parametrize("code", [99, 0, 600, 1000, -1])
def test_out_of_range_raises(code):
    with pytest.raises(ValueError):
        classify_status(code)
