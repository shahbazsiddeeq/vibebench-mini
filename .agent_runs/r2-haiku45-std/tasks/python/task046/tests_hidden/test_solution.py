import pytest
from src.solution import to_morse


















FULL_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}


def test_single_letter():
    assert to_morse("S") == "..."


def test_word():
    assert to_morse("HI") == ".... .."


def test_lowercase_same():
    assert to_morse("sos") == to_morse("SOS")


def test_unknown_raises():
    with pytest.raises(ValueError):
        to_morse("Hello!")


@pytest.mark.parametrize("ch,code", list(FULL_TABLE.items()))
def test_every_symbol(ch, code):
    assert to_morse(ch) == code


def test_all_digits():
    digits = "0123456789"
    expected = " ".join(FULL_TABLE[c] for c in digits)
    assert to_morse(digits) == expected
