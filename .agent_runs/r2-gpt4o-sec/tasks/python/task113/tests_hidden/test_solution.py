import pytest
from src.solution import from_roman














def _to_roman(n: int) -> str:
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, sym in table:
        while n >= value:
            out.append(sym)
            n -= value
    return "".join(out)


def test_basic():
    assert from_roman("XIV") == 14
    assert from_roman("IV") == 4
    assert from_roman("IX") == 9


def test_single():
    assert from_roman("I") == 1
    assert from_roman("M") == 1000


def test_invalid_char():
    with pytest.raises(ValueError):
        from_roman("ABC")


def test_roundtrip_against_encoder():
    for n in range(1, 4000):
        assert from_roman(_to_roman(n)) == n
