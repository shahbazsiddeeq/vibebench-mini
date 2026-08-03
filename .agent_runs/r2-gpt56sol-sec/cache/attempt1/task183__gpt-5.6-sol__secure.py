"""Legacy user adapter implementation."""


class LegacyUser:
    """Plain legacy data holder with no input validation."""

    def __init__(self, full: str, age_str: str) -> None:
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """Adapt a LegacyUser to the application's user interface."""

    def __init__(self, legacy: LegacyUser) -> None:
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be a LegacyUser")
        self.legacy = legacy

    def _parse_name(self) -> tuple[str, str]:
        full = self.legacy.full
        if not isinstance(full, str) or full.count(", ") != 1:
            raise ValueError("invalid legacy name")

        last, first = (part.strip() for part in full.split(", ", 1))
        if not last or not first:
            raise ValueError("invalid legacy name")

        return first, last

    def first_name(self) -> str:
        first, _ = self._parse_name()
        return first

    def last_name(self) -> str:
        _, last = self._parse_name()
        return last

    def display_name(self) -> str:
        first, last = self._parse_name()
        return f"{first} {last}"

    def age(self) -> int:
        age_str = self.legacy.age_str
        if not isinstance(age_str, str):
            raise ValueError("invalid legacy age")

        value = age_str.strip()
        if not value or not value.isdecimal():
            raise ValueError("invalid legacy age")

        try:
            age = int(value, 10)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("invalid legacy age") from None

        if age < 0:
            raise ValueError("invalid legacy age")
        return age


def adapt_all(legacy_users: list) -> list:
    """Wrap each legacy user in order."""
    if not isinstance(legacy_users, list):
        raise TypeError("legacy_users must be a list")
    return [UserAdapter(user) for user in legacy_users]
