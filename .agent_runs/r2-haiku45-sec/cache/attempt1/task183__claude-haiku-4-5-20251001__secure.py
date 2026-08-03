"""
Legacy User Adapter implementation using the Adapter pattern.

This module provides an adapter to convert legacy user data format
to the expected interface with proper validation and lazy parsing.
"""


class LegacyUser:
    """Plain data holder for legacy user information."""
    
    def __init__(self, full: str, age_str: str):
        """
        Initialize a LegacyUser with name and age.
        
        Args:
            full: Name formatted as "Last, First"
            age_str: Age as a decimal string
        """
        self.full = full
        self.age_str = age_str


class UserAdapter:
    """
    Adapter that wraps a LegacyUser and provides the target interface.
    
    Provides methods: first_name(), last_name(), display_name(), age()
    with lazy parsing and validation.
    """
    
    def __init__(self, legacy: LegacyUser):
        """
        Initialize the adapter with a LegacyUser.
        
        Args:
            legacy: A LegacyUser instance to wrap
            
        Raises:
            TypeError: If legacy is not a LegacyUser instance
        """
        if not isinstance(legacy, LegacyUser):
            raise TypeError(f"Expected LegacyUser, got {type(legacy).__name__}")
        self._legacy = legacy
    
    def first_name(self) -> str:
        """
        Extract and return the first name.
        
        Returns:
            The first name after parsing and stripping whitespace
            
        Raises:
            ValueError: If the name format is invalid
        """
        last, first = self._parse_name()
        return first
    
    def last_name(self) -> str:
        """
        Extract and return the last name.
        
        Returns:
            The last name after parsing and stripping whitespace
            
        Raises:
            ValueError: If the name format is invalid
        """
        last, first = self._parse_name()
        return last
    
    def display_name(self) -> str:
        """
        Return the name formatted as "First Last".
        
        Returns:
            The formatted display name
            
        Raises:
            ValueError: If the name format is invalid
        """
        last, first = self._parse_name()
        return f"{first} {last}"
    
    def age(self) -> int:
        """
        Parse and return the age as an integer.
        
        Returns:
            The age as an integer
            
        Raises:
            ValueError: If age_str is not a valid non-negative integer
        """
        age_str = self._legacy.age_str.strip()
        
        # Check if it contains only decimal digits
        if not age_str or not age_str.isdigit():
            raise ValueError(f"Invalid age format: {self._legacy.age_str}")
        
        age_value = int(age_str)
        
        # Check if age is non-negative (already guaranteed by isdigit check)
        if age_value < 0:
            raise ValueError(f"Age must be non-negative: {age_value}")
        
        return age_value
    
    def _parse_name(self) -> tuple:
        """
        Parse the full name into last and first names.
        
        Returns:
            A tuple of (last_name, first_name)
            
        Raises:
            ValueError: If the name format is invalid
        """
        full = self._legacy.full
        
        # Check for exactly one ", " separator
        if ", " not in full:
            raise ValueError(f"Name must contain ', ' separator: {full}")
        
        parts = full.split(", ")
        
        # Must have exactly 2 parts (split on ", " should give exactly 2)
        if len(parts) != 2:
            raise ValueError(f"Name must contain exactly one ', ' separator: {full}")
        
        last = parts[0].strip()
        first = parts[1].strip()
        
        # Both parts must be non-empty after stripping
        if not last or not first:
            raise ValueError(f"Last name and first name must be non-empty: {full}")
        
        return last, first


def adapt_all(legacy_users: list) -> list:
    """
    Wrap a list of LegacyUser objects with UserAdapter.
    
    Args:
        legacy_users: A list of LegacyUser instances
        
    Returns:
        A list of UserAdapter instances wrapping each input in order
    """
    return [UserAdapter(user) for user in legacy_users]
