"""
Legacy User Adapter module.

Implements the Adapter design pattern to expose a modern interface
(first_name, last_name, display_name, age) over a legacy user data
structure (LegacyUser) that stores raw, unvalidated strings.

Parsing/validation is performed lazily inside the adapter methods,
never during construction.
"""

from typing import List


class LegacyUser:
    """Plain legacy data holder with no validation."""

    __slots__ = ("full", "age_str")

    def __init__(self, full: str, age_str: str) -> None:
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """Adapts a LegacyUser to the target interface expected by the app."""

    __slots__ = ("_legacy",)

    def __init__(self, legacy: LegacyUser) -> None:
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be an instance of LegacyUser")
        self._legacy = legacy

    def _split_name(self):
        full = self._legacy.full
        if not isinstance(full, str):
            raise ValueError("Invalid legacy name: expected a string")

        parts = full.split(", ")
        if len(parts) != 2:
            raise ValueError(
                "Invalid legacy name format: expected exactly one ', ' separator"
            )

        last, first = parts
        last = last.strip()
        first = first.strip()

        if not last or not first:
            raise ValueError("Invalid legacy name: last and first names must be non-empty")

        return last, first

    def first_name(self) -> str:
        _, first = self._split_name()
        return first

    def last_name(self) -> str:
        last, _ = self._split_name()
        return last

    def display_name(self) -> str:
        last, first = self._split_name()
        return f"{first} {last}"

    def age(self) -> int:
        age_str = self._legacy.age_str
        if not isinstance(age_str, str):
            raise ValueError("Invalid legacy age: expected a string")

        stripped = age_str.strip()
        if not stripped.isdigit():
            raise ValueError("Invalid legacy age: must consist only of decimal digits")

        value = int(stripped)
        if value < 0:
            raise ValueError("Invalid legacy age: must be >= 0")

        return value


def adapt_all(legacy_users: list) -> List[UserAdapter]:
    """Wrap each element of legacy_users in a UserAdapter, preserving order."""
    if not isinstance(legacy_users, list):
        raise TypeError("legacy_users must be a list")
    return [UserAdapter(u) for u in legacy_users]
