# src/solution.py

class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str


class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("Expected a LegacyUser instance")
        self._legacy = legacy

    def first_name(self) -> str:
        return self._parse_name()[1]

    def last_name(self) -> str:
        return self._parse_name()[0]

    def display_name(self) -> str:
        first, last = self._parse_name()
        return f"{first} {last}"

    def age(self) -> int:
        age_str = self._legacy.age_str.strip()
        if not age_str.isdigit() or int(age_str) < 0:
            raise ValueError("Invalid age")
        return int(age_str)

    def _parse_name(self):
        full = self._legacy.full.strip()
        if ", " not in full or full.count(", ") != 1:
            raise ValueError("Invalid name format")
        last, first = map(str.strip, full.split(", "))
        if not last or not first:
            raise ValueError("Invalid name format")
        return last, first


def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(user) for user in legacy_users]
