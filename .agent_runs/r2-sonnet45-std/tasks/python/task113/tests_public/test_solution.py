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


def test_large():
    assert from_roman("MMXXIV") == 2024
    assert from_roman("MCMXCIX") == 1999


def test_empty():
    with pytest.raises(ValueError):
        from_roman("")


def test_l_and_d_symbols():
    # Guards against swapping entries for symbols not otherwise exercised.
    assert from_roman("L") == 50
    assert from_roman("D") == 500
    assert from_roman("LXIV") == 64
    assert from_roman("XL") == 40
    assert from_roman("CD") == 400
    assert from_roman("DCCCXC") == 890
