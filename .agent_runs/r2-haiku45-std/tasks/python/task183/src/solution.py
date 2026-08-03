class LegacyUser:
    """A legacy component that holds user data with minimal validation."""
    
    def __init__(self, full: str, age_str: str):
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """Adapter that wraps a LegacyUser and provides the target interface."""
    
    def __init__(self, legacy: LegacyUser):
        if not isinstance(legacy, LegacyUser):
            raise TypeError(f"Expected LegacyUser, got {type(legacy)}")
        self._legacy = legacy
    
    def first_name(self) -> str:
        """Extract and return the first name from the legacy user's full name."""
        parts = self._parse_name()
        return parts[1]
    
    def last_name(self) -> str:
        """Extract and return the last name from the legacy user's full name."""
        parts = self._parse_name()
        return parts[0]
    
    def display_name(self) -> str:
        """Return the name formatted as 'First Last'."""
        parts = self._parse_name()
        return f"{parts[1]} {parts[0]}"
    
    def age(self) -> int:
        """Parse and return the age as an integer."""
        age_str = self._legacy.age_str.strip()
        
        # Check if it consists only of decimal digits
        if not age_str or not age_str.isdigit():
            raise ValueError(f"Invalid age string: {self._legacy.age_str}")
        
        age_value = int(age_str)
        
        # Check if age is >= 0
        if age_value < 0:
            raise ValueError(f"Age must be >= 0, got {age_value}")
        
        return age_value
    
    def _parse_name(self) -> tuple:
        """
        Parse the full name and return (last_name, first_name).
        Raises ValueError if the format is invalid.
        """
        full = self._legacy.full
        
        # Check if it contains exactly one ", " separator
        if ", " not in full:
            raise ValueError(f"Name must contain ', ' separator: {full}")
        
        parts = full.split(", ")
        
        # Must have exactly 2 parts (one separator)
        if len(parts) != 2:
            raise ValueError(f"Name must contain exactly one ', ' separator: {full}")
        
        last_name = parts[0].strip()
        first_name = parts[1].strip()
        
        # Both parts must be non-empty after stripping
        if not last_name or not first_name:
            raise ValueError(f"Last name and first name must be non-empty: {full}")
        
        return (last_name, first_name)


def adapt_all(legacy_users: list) -> list:
    """Convert a list of LegacyUser objects to a list of UserAdapter objects."""
    return [UserAdapter(user) for user in legacy_users]
