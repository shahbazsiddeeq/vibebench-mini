import pytest
from src.solution import classify_status


def test_success():
    assert classify_status(200) == "success"


def test_client_error():
    assert classify_status(404) == "client_error"


def test_unknown_raises():
    with pytest.raises(ValueError):
        classify_status(999)


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


@pytest.mark.parametrize("code", [99, 0, 600, 1000, -1])
def test_out_of_range_raises(code):
    with pytest.raises(ValueError):
        classify_status(code)
