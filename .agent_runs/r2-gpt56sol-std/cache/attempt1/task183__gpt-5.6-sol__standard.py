class LegacyUser:
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str


class UserAdapter:
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be a LegacyUser")
        self.legacy = legacy

    def _parse_name(self) -> tuple[str, str]:
        full = self.legacy.full
        if not isinstance(full, str) or full.count(", ") != 1:
            raise ValueError("invalid full name")

        last, first = (part.strip() for part in full.split(", "))
        if not last or not first:
            raise ValueError("invalid full name")

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
            raise ValueError("invalid age")

        stripped = age_str.strip()
        if not stripped or not stripped.isdecimal():
            raise ValueError("invalid age")

        value = int(stripped)
        if value < 0:
            raise ValueError("invalid age")
        return value


def adapt_all(legacy_users: list) -> list:
    return [UserAdapter(user) for user in legacy_users]
