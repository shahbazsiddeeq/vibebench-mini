def natural_sort(items):
    """
    Sort strings in natural order where embedded digit sequences are compared numerically.
    
    Args:
        items: List of strings to sort
        
    Returns:
        New list with strings sorted in natural order
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    
    # Validate all items are strings
    for item in items:
        if not isinstance(item, str):
            raise TypeError("all items must be strings")
    
    def parse_key(s):
        """
        Parse a string into a list of tuples for comparison.
        Each tuple is (is_numeric, value) where:
        - is_numeric=False means it's a text run (value is the string)
        - is_numeric=True means it's a numeric run (value is the integer)
        
        Numeric runs sort before text runs at the same position (False < True).
        """
        if not s:
            return []
        
        result = []
        i = 0
        n = len(s)
        
        while i < n:
            if s[i].isdigit():
                # Collect all consecutive digits
                j = i
                while j < n and s[j].isdigit():
                    j += 1
                # Convert to integer for numeric comparison
                # Use False for numeric runs so they sort before text runs
                result.append((False, int(s[i:j])))
                i = j
            else:
                # Collect all consecutive non-digits
                j = i
                while j < n and not s[j].isdigit():
                    j += 1
                # Use True for text runs so they sort after numeric runs
                result.append((True, s[i:j]))
                i = j
        
        return result
    
    # Create a new list to avoid modifying the input
    return sorted(items, key=parse_key)
