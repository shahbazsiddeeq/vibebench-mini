def natural_sort(items):
    """
    Sort strings in natural order where numeric runs are compared by value.
    
    Args:
        items: List of strings to sort
        
    Returns:
        New list with strings sorted in natural order
    """
    def parse_key(s):
        """
        Parse a string into a list of (is_digit, value) tuples.
        is_digit is True for numeric runs, False for text runs.
        value is the integer for numeric runs, the string for text runs.
        """
        if not s:
            return []
        
        result = []
        i = 0
        while i < len(s):
            if s[i].isdigit():
                # Collect all consecutive digits
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                # Store as (True, numeric_value)
                result.append((True, int(s[i:j])))
                i = j
            else:
                # Collect all consecutive non-digits
                j = i
                while j < len(s) and not s[j].isdigit():
                    j += 1
                # Store as (False, text_string)
                result.append((False, s[i:j]))
                i = j
        
        return result
    
    def compare_keys(key1, key2):
        """
        Compare two parsed keys.
        Returns -1 if key1 < key2, 0 if equal, 1 if key1 > key2.
        """
        # Compare element by element
        for i in range(min(len(key1), len(key2))):
            is_digit1, val1 = key1[i]
            is_digit2, val2 = key2[i]
            
            # If both are the same type, compare values
            if is_digit1 == is_digit2:
                if val1 < val2:
                    return -1
                elif val1 > val2:
                    return 1
                # Equal, continue to next element
            else:
                # Different types: digit runs sort before text runs
                if is_digit1:  # key1 is digit, key2 is text
                    return -1
                else:  # key1 is text, key2 is digit
                    return 1
        
        # All compared elements are equal, shorter key comes first
        if len(key1) < len(key2):
            return -1
        elif len(key1) > len(key2):
            return 1
        else:
            return 0
    
    # Create a list of (original_index, parsed_key, original_string) tuples
    # to maintain stability
    indexed_items = [(i, parse_key(s), s) for i, s in enumerate(items)]
    
    # Sort using the comparison function
    from functools import cmp_to_key
    
    def compare_items(item1, item2):
        idx1, key1, s1 = item1
        idx2, key2, s2 = item2
        
        cmp_result = compare_keys(key1, key2)
        if cmp_result != 0:
            return cmp_result
        
        # If keys are equal, maintain stability by comparing original indices
        return idx1 - idx2
    
    sorted_items = sorted(indexed_items, key=cmp_to_key(compare_items))
    
    # Extract just the strings
    return [s for _, _, s in sorted_items]
