import pytest

from src.solution import LegacyUser, UserAdapter, adapt_all


def test_worked_example():
    u = UserAdapter(LegacyUser("Doe, John", "42"))
    assert u.first_name() == "John"
    assert u.last_name() == "Doe"
    assert u.display_name() == "John Doe"
    assert u.age() == 42


def test_strips_whitespace_in_age():
    assert UserAdapter(LegacyUser("A, B", "  7 ")).age() == 7


def test_adapter_wraps_not_copies():
    legacy = LegacyUser("Old, Value", "1")
    u = UserAdapter(legacy)
    # Adapter reads through to the adaptee lazily; mutating the adaptee is reflected.
    legacy.full = "New, Name"
    legacy.age_str = "99"
    assert u.display_name() == "Name New"
    assert u.age() == 99


def test_wrong_adaptee_type_raises():
    with pytest.raises(TypeError):
        UserAdapter("Doe, John")
    with pytest.raises(TypeError):
        UserAdapter({"full": "Doe, John"})


def test_invalid_age_raises():
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "abc")).age()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "-3")).age()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "")).age()
