import pytest

from src.solution import vigenere_encrypt, vigenere_decrypt


def test_worked_example():
    assert vigenere_encrypt("Attack at Dawn!", "LEMON") == "Lxfopv ef Rnhr!"


def test_uppercase_classic_vector():
    # HELLO with key KEY -> RIJVS (hardcoded, standard textbook vector)
    assert vigenere_encrypt("HELLO", "KEY") == "RIJVS"
    assert vigenere_decrypt("RIJVS", "KEY") == "HELLO"


def test_key_case_insensitive():
    assert vigenere_encrypt("HELLO", "key") == vigenere_encrypt("HELLO", "KEY")
    assert vigenere_encrypt("HELLO", "KeY") == "RIJVS"


def test_z_wraparound():
    # 'z' shifted by 'b' (1) wraps to 'a'; 'Z' by 'B' wraps to 'A'.
    assert vigenere_encrypt("zZ", "B") == "aA"


def test_non_ascii_letters_passthrough():
    # Accented / non-ASCII letters are copied unchanged and do not advance key.
    assert vigenere_encrypt("abécd", "B") == "bcéde"


def test_empty_text_ok():
    assert vigenere_encrypt("", "KEY") == ""
    assert vigenere_decrypt("", "KEY") == ""


def test_value_errors_empty_key():
    with pytest.raises(ValueError):
        vigenere_encrypt("HELLO", "")
    with pytest.raises(ValueError):
        vigenere_decrypt("HELLO", "")


def test_type_check_precedes_key_length_check():
    # Non-str text with an (also invalid) empty key must raise TypeError, not ValueError.
    with pytest.raises(TypeError):
        vigenere_encrypt(123, "")
