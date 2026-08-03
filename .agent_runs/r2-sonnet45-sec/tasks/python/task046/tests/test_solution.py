import pytest
from src.solution import to_morse


def test_single_letter():
    assert to_morse("S") == "..."


def test_sos():
    assert to_morse("SOS") == "... --- ..."


def test_word():
    assert to_morse("HI") == ".... .."


def test_two_words():
    assert to_morse("HELLO WORLD") == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."


def test_lowercase_same():
    assert to_morse("sos") == to_morse("SOS")


def test_digit():
    assert to_morse("1") == ".----"


def test_unknown_raises():
    with pytest.raises(ValueError):
        to_morse("Hello!")


def test_single_digit_word():
    assert to_morse("5") == "....."


FULL_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}


@pytest.mark.parametrize("ch,code", list(FULL_TABLE.items()))
def test_every_symbol(ch, code):
    assert to_morse(ch) == code


def test_whole_alphabet_in_order():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    expected = " ".join(FULL_TABLE[c] for c in letters)
    assert to_morse(letters) == expected


def test_all_digits():
    digits = "0123456789"
    expected = " ".join(FULL_TABLE[c] for c in digits)
    assert to_morse(digits) == expected
