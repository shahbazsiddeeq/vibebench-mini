import pytest

from src.solution import LegacyUser, UserAdapter, adapt_all


def test_worked_example():
    u = UserAdapter(LegacyUser("Doe, John", "42"))
    assert u.first_name() == "John"
    assert u.last_name() == "Doe"
    assert u.display_name() == "John Doe"
    assert u.age() == 42


def test_strips_whitespace_in_name():
    u = UserAdapter(LegacyUser("  Smith ,  Jane ", "30"))
    assert u.first_name() == "Jane"
    assert u.last_name() == "Smith"
    assert u.display_name() == "Jane Smith"


def test_strips_whitespace_in_age():
    assert UserAdapter(LegacyUser("A, B", "  7 ")).age() == 7


def test_age_zero():
    assert UserAdapter(LegacyUser("A, B", "0")).age() == 0


def test_adapter_wraps_not_copies():
    legacy = LegacyUser("Old, Value", "1")
    u = UserAdapter(legacy)
    # Adapter reads through to the adaptee lazily; mutating the adaptee is reflected.
    legacy.full = "New, Name"
    legacy.age_str = "99"
    assert u.display_name() == "Name New"
    assert u.age() == 99


def test_adapt_all():
    users = [LegacyUser("Doe, John", "42"), LegacyUser("Roe, Jane", "31")]
    adapters = adapt_all(users)
    assert [a.display_name() for a in adapters] == ["John Doe", "Jane Roe"]
    assert all(isinstance(a, UserAdapter) for a in adapters)


def test_wrong_adaptee_type_raises():
    with pytest.raises(TypeError):
        UserAdapter("Doe, John")
    with pytest.raises(TypeError):
        UserAdapter({"full": "Doe, John"})


def test_malformed_name_raises():
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("NoSeparator", "1")).first_name()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B, C", "1")).display_name()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser(", John", "1")).last_name()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("Doe, ", "1")).first_name()


def test_invalid_age_raises():
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "abc")).age()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "-3")).age()
    with pytest.raises(ValueError):
        UserAdapter(LegacyUser("A, B", "")).age()


def test_construction_does_not_validate():
    # Lazy parsing: constructing over bad data must not raise.
    UserAdapter(LegacyUser("garbage", "garbage"))
