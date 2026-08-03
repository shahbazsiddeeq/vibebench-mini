from src.solution import check_password


def test_strong_password():
    result = check_password("Abc123!x")
    assert result["score"] == 5


def test_length_field():
    result = check_password("hello")
    assert result["length"] == 5


def test_has_lower():
    assert check_password("abc")["has_lower"] is True


def test_has_special():
    assert check_password("!")["has_special"] is True


def test_length_criterion_7_not_counted():
    # 7 lowercase letters: only has_lower -> exactly 1.
    result = check_password("abcdefg")
    assert result["length"] == 7
    assert result["score"] == 1


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
