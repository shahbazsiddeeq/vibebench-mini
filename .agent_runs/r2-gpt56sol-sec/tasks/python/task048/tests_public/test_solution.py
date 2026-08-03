from src.solution import check_password


def test_weak_password():
    result = check_password("abc")
    assert result["score"] == 1
    assert result["has_lower"] is True
    assert result["has_upper"] is False


def test_has_upper():
    assert check_password("ABC")["has_upper"] is True


def test_has_digit():
    assert check_password("123")["has_digit"] is True


def test_length_criterion_exactly_8():
    # 8 lowercase letters: has_lower + length>=8 -> exactly 2.
    result = check_password("abcdefgh")
    assert result["score"] == 2


def test_special_char_set():
    # A punctuation character counts; a plain letter/digit does not.
    assert check_password("@")["has_special"] is True
    assert check_password("a1")["has_special"] is False
