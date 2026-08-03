class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str

class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("Input must be an instance of LegacyUser")
        self._legacy = legacy
        self._first_name = None
        self._last_name = None
        self._age = None

    def _parse_name(self):
        if self._first_name is not None and self._last_name is not None:
            return

        full_stripped = self._legacy.full.strip()
        parts = full_stripped.split(", ")

        if len(parts) != 2:
            raise ValueError("Name must contain exactly one ', ' separator.")

        last_name_raw = parts[0].strip()
        first_name_raw = parts[1].strip()

        if not last_name_raw:
            raise ValueError("Last name cannot be empty.")
        if not first_name_raw:
            raise ValueError("First name cannot be empty.")

        self._last_name = last_name_raw
        self._first_name = first_name_raw

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
            raise ValueError("Age string must consist only of decimal digits.")

        parsed_age = int(age_str_stripped)
        if parsed_age < 0:
            raise ValueError("Age cannot be negative.")

        self._age = parsed_age
        return self._age

def adapt_all(legacy_users: list) -> list:
    if not isinstance(legacy_users, list):
        raise TypeError("Input must be a list.")
    
    adapted_users = []
    for user in legacy_users:
        # UserAdapter constructor already validates the type of 'user'
        adapted_users.append(UserAdapter(user))
    return adapted_users
