import pytest

from src.solution import pbkdf2_hash, verify_password


# Published PBKDF2-HMAC-SHA256 test vectors (password="password", salt="salt").
# These are hardcoded literals, not recomputed with hashlib.
VEC_1 = "120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b"
VEC_2 = "ae4d0c95af6b46d32d0adff928f06dd02a303f8ef3c251dfd6e2d85a95474c43"
VEC_4096 = "c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a"


def test_vector_iterations_1():
    assert pbkdf2_hash("password", b"salt", 1, 32) == VEC_1


def test_vector_iterations_4096():
    assert pbkdf2_hash("password", b"salt", 4096, 32) == VEC_4096


def test_custom_dklen_length():
    assert len(pbkdf2_hash("password", b"salt", 1, 16)) == 32


def test_mutation_iterations_changes_output():
    # Guards against ignoring the iterations argument.
    assert pbkdf2_hash("password", b"salt", 1, 32) != pbkdf2_hash(
        "password", b"salt", 2, 32
    )


def test_verify_accepts_correct():
    assert verify_password("password", b"salt", 1, VEC_1) is True


def test_verify_rejects_wrong_iterations():
    assert verify_password("password", b"salt", 2, VEC_1) is False


def test_verify_non_ascii_password():
    salt = b"pepper"
    h = pbkdf2_hash("pässwörd", salt, 3, 32)
    assert verify_password("pässwörd", salt, 3, h) is True
    assert verify_password("passwrd", salt, 3, h) is False


def test_value_errors():
    with pytest.raises(ValueError):
        pbkdf2_hash("password", b"salt", 0, 32)
    with pytest.raises(ValueError):
        pbkdf2_hash("password", b"salt", 1, 0)
