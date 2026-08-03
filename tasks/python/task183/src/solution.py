from __future__ import annotations


class LegacyUser:
    """Adaptee: a legacy record with an incompatible interface."""

    def __init__(self, full: str, age_str: str) -> None:
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """Adapts a LegacyUser to the target user interface."""

    def __init__(self, legacy: LegacyUser) -> None:
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be a LegacyUser")
        self._legacy = legacy

    def _split_name(self) -> tuple[str, str]:
        parts = self._legacy.full.split(", ")
        if len(parts) != 2:
            raise ValueError(f"malformed name: {self._legacy.full!r}")
        last, first = parts[0].strip(), parts[1].strip()
        if not last or not first:
            raise ValueError(f"malformed name: {self._legacy.full!r}")
        return first, last

    def first_name(self) -> str:
        return self._split_name()[0]

    def last_name(self) -> str:
        return self._split_name()[1]

    def display_name(self) -> str:
        first, last = self._split_name()
        return f"{first} {last}"

    def age(self) -> int:
        raw = self._legacy.age_str.strip()
        if not raw.isdigit():
            raise ValueError(f"invalid age: {self._legacy.age_str!r}")
        return int(raw)


def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(u) for u in legacy_users]
