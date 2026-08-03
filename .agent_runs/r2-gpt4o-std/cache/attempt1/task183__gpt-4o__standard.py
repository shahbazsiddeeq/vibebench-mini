# src/solution.py

class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str

class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("Expected a LegacyUser instance")
        self.legacy = legacy

    def first_name(self) -> str:
        last, first = self._parse_full_name()
        return first

    def last_name(self) -> str:
        last, first = self._parse_full_name()
        return last

    def display_name(self) -> str:
        last, first = self._parse_full_name()
        return f"{first} {last}"

    def age(self) -> int:
        age_str = self.legacy.age_str.strip()
        if not age_str.isdigit():
            raise ValueError("Age must be a non-negative integer")
        return int(age_str)

    def _parse_full_name(self):
        parts = self.legacy.full.split(",")
        if len(parts) != 2:
            raise ValueError("Full name must contain exactly one ', ' separator")
        last, first = parts
        last = last.strip()
        first = first.strip()
        if not last or not first:
            raise ValueError("First and last names must be non-empty")
        return last, first

def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(user) for user in legacy_users]
