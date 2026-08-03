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


def test_sos():
    assert to_morse("SOS") == "... --- ..."


def test_two_words():
    assert to_morse("HELLO WORLD") == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."


def test_digit():
    assert to_morse("1") == ".----"


def test_single_digit_word():
    assert to_morse("5") == "....."


def test_whole_alphabet_in_order():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    expected = " ".join(FULL_TABLE[c] for c in letters)
    assert to_morse(letters) == expected
