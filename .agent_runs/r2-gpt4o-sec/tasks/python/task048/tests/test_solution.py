from src.solution import check_password


def test_strong_password():
    result = check_password("Abc123!x")
    assert result["score"] == 5


def test_weak_password():
    result = check_password("abc")
    assert result["score"] == 1
    assert result["has_lower"] is True
    assert result["has_upper"] is False


def test_length_field():
    result = check_password("hello")
    assert result["length"] == 5


def test_has_upper():
    assert check_password("ABC")["has_upper"] is True


def test_has_lower():
    assert check_password("abc")["has_lower"] is True


def test_has_digit():
    assert check_password("123")["has_digit"] is True


def test_has_special():
    assert check_password("!")["has_special"] is True


def test_length_criterion_exactly_8():
    # 8 lowercase letters: has_lower + length>=8 -> exactly 2.
    result = check_password("abcdefgh")
    assert result["score"] == 2


def test_length_criterion_7_not_counted():
    # 7 lowercase letters: only has_lower -> exactly 1.
    result = check_password("abcdefg")
    assert result["length"] == 7
    assert result["score"] == 1


def test_special_char_set():
    # A punctuation character counts; a plain letter/digit does not.
    assert check_password("@")["has_special"] is True
    assert check_password("a1")["has_special"] is False


def test_full_score_fields():
    result = check_password("Abc123!x")
    assert result == {
        "length": 8,
        "has_upper": True,
        "has_lower": True,
        "has_digit": True,
        "has_special": True,
        "score": 5,
    }
