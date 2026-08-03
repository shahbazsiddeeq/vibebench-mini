class LegacyUser:
    """Legacy component: plain data holder with no validation."""
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """Adapter that wraps LegacyUser and provides the target interface."""
    
    def __init__(self, legacy):
        if not isinstance(legacy, LegacyUser):
            raise TypeError("legacy must be a LegacyUser instance")
        self._legacy = legacy
    
    def _parse_name(self):
        """Parse and validate the full name. Returns (last_name, first_name)."""
        full = self._legacy.full
        
        # Check for exactly one ", " separator
        if full.count(", ") != 1:
            raise ValueError("Name must contain exactly one ', ' separator")
        
        # Split on ", "
        parts = full.split(", ")
        last = parts[0].strip()
        first = parts[1].strip()
        
        # Both parts must be non-empty after stripping
        if not last or not first:
            raise ValueError("Both first and last name must be non-empty")
        
        return last, first
    
    def first_name(self) -> str:
        """Return the first name."""
        _, first = self._parse_name()
        return first
    
    def last_name(self) -> str:
        """Return the last name."""
        last, _ = self._parse_name()
        return last
    
    def display_name(self) -> str:
        """Return the display name formatted as 'First Last'."""
        last, first = self._parse_name()
        return f"{first} {last}"
    
    def age(self) -> int:
        """Parse and return the age as an integer."""
        age_str = self._legacy.age_str.strip()
        
        # Must consist only of decimal digits
        if not age_str.isdigit():
            raise ValueError("Age must consist only of decimal digits")
        
        age_value = int(age_str)
        
        # Must be >= 0 (already guaranteed by isdigit() which excludes negative signs)
        if age_value < 0:
            raise ValueError("Age must be >= 0")
        
        return age_value


def adapt_all(legacy_users: list) -> list:
    """Wrap each LegacyUser in the list with a UserAdapter."""
    return [UserAdapter(user) for user in legacy_users]
