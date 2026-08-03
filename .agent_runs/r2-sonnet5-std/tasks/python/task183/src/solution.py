# src/solution.py

class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str


class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be an instance of LegacyUser")
        self._legacy = legacy

    def _parse_name(self):
        full = self._legacy.full
        parts = full.split(", ")
        if len(parts) != 2:
            raise ValueError("full name must contain exactly one ', ' separator")
        last, first = parts[0].strip(), parts[1].strip()
        if not last or not first:
            raise ValueError("last name and first name must be non-empty")
        return last, first

    def first_name(self) -> str:
        _, first = self._parse_name()
        return first

    def last_name(self) -> str:
        last, _ = self._parse_name()
        return last

    def display_name(self) -> str:
        last, first = self._parse_name()
        return f"{first} {last}"

    def age(self) -> int:
        age_str = self._legacy.age_str.strip()
        if not age_str.isdigit():
            raise ValueError("age_str must consist only of decimal digits")
        value = int(age_str)
        if value < 0:
            raise ValueError("age must be >= 0")
        return value


def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(u) for u in legacy_users]
