import pytest

from src.solution import vigenere_encrypt, vigenere_decrypt


def test_decrypt_worked_example():
    assert vigenere_decrypt("Lxfopv ef Rnhr!", "LEMON") == "Attack at Dawn!"


def test_case_preserved_and_passthrough():
    assert vigenere_encrypt("Hello, World!", "abc") == "Hfnlp, Yosnd!"
    assert vigenere_decrypt("Hfnlp, Yosnd!", "abc") == "Hello, World!"


def test_non_letters_do_not_advance_key():
    # Key "B" shifts every letter by +1; separators must not consume key positions.
    assert vigenere_encrypt("az AZ 9!", "B") == "ba BA 9!"


def test_zero_shift_key_a_is_identity_on_letters():
    assert vigenere_encrypt("Hello, World 123!", "A") == "Hello, World 123!"


def test_roundtrip_various():
    key = "SecretKey"
    for text in ["The quick brown fox.", "MixEd CaSe 42!!", "", "   ", "ZZZZ zzzz"]:
        assert vigenere_decrypt(vigenere_encrypt(text, key), key) == text


def test_type_errors():
    with pytest.raises(TypeError):
        vigenere_encrypt(123, "KEY")
    with pytest.raises(TypeError):
        vigenere_encrypt("HELLO", 5)
    with pytest.raises(TypeError):
        vigenere_decrypt(None, "KEY")


def test_value_errors_bad_key_chars():
    with pytest.raises(ValueError):
        vigenere_encrypt("HELLO", "ke y")
    with pytest.raises(ValueError):
        vigenere_encrypt("HELLO", "key1")
    with pytest.raises(ValueError):
        vigenere_decrypt("HELLO", "k-y")


def test_mutation_killer_key_alignment():
    # If a non-letter incorrectly advanced the key, the letters after the space would
    # differ. This exact literal pins correct alignment across the boundary.
    assert vigenere_encrypt("abcde fghij", "LEMON") == "lforr qktww"
