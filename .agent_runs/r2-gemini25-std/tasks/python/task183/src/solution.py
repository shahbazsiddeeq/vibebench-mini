class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str

class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be an instance of LegacyUser")
        self._legacy = legacy
        self._first_name = None
        self._last_name = None
        self._age = None

    def _parse_name(self):
        if self._first_name is not None and self._last_name is not None:
            return

        parts = self._legacy.full.split(',')
        if len(parts) != 2:
            raise ValueError("Invalid name format: must contain exactly one ', ' separator")

        last_name = parts[0].strip()
        first_name = parts[1].strip()

        if not last_name or not first_name:
            raise ValueError("Invalid name format: first and last names cannot be empty")

        self._last_name = last_name
        self._first_name = first_name

    def first_name(self) -> str:
        self._parse_name()
        return self._first_name

    def last_name(self) -> str:
        self._parse_name()
        return self._last_name

    def display_name(self) -> str:
        self._parse_name()
        return f"{self._first_name} {self._last_name}"

    def age(self) -> int:
        if self._age is not None:
            return self._age

        age_str_stripped = self._legacy.age_str.strip()
        if not age_str_stripped.isdigit():
            raise ValueError("Invalid age format: must contain only decimal digits")

        parsed_age = int(age_str_stripped)
        if parsed_age < 0:
            raise ValueError("Invalid age: must be a non-negative value")

        self._age = parsed_age
        return self._age

def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(user) for user in legacy_users]
