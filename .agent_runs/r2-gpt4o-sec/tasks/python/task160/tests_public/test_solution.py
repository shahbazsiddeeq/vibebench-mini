import pytest

from src.solution import pbkdf2_hash, verify_password


# Published PBKDF2-HMAC-SHA256 test vectors (password="password", salt="salt").
# These are hardcoded literals, not recomputed with hashlib.
VEC_1 = "120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b"
VEC_2 = "ae4d0c95af6b46d32d0adff928f06dd02a303f8ef3c251dfd6e2d85a95474c43"
VEC_4096 = "c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a"


def test_vector_iterations_2():
    assert pbkdf2_hash("password", b"salt", 2, 32) == VEC_2


def test_default_dklen_is_32_bytes():
    assert len(pbkdf2_hash("password", b"salt", 1)) == 64


def test_output_is_lowercase_hex():
    out = pbkdf2_hash("password", b"salt", 1, 32)
    assert out == out.lower()
    assert all(c in "0123456789abcdef" for c in out)


def test_mutation_salt_changes_output():
    assert pbkdf2_hash("password", b"salt", 1, 32) != pbkdf2_hash(
        "password", b"NaCl", 1, 32
    )


def test_verify_rejects_wrong_password():
    assert verify_password("Password", b"salt", 1, VEC_1) is False


def test_verify_case_insensitive_hex():
    assert verify_password("password", b"salt", 1, VEC_1.upper()) is True


def test_type_errors():
    with pytest.raises(TypeError):
        pbkdf2_hash(b"password", b"salt", 1, 32)
    with pytest.raises(TypeError):
        pbkdf2_hash("password", "salt", 1, 32)
    with pytest.raises(TypeError):
        pbkdf2_hash("password", b"salt", True, 32)


def test_verify_bad_hex_raises():
    with pytest.raises(ValueError):
        verify_password("password", b"salt", 1, "not-hex")
