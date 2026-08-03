def number_to_words(n: int) -> str:
    """
    Convert an integer to its English word representation.
    
    Args:
        n: An integer in the range [-999999999999, 999999999999]
    
    Returns:
        A string representation of the number in lowercase English words
    
    Raises:
        TypeError: If n is not an int (bool is rejected)
        ValueError: If n is outside the supported range
    """
    # Type validation - reject bool explicitly since bool is a subclass of int
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    
    # Range validation
    if n < -999999999999 or n > 999999999999:
        raise ValueError(f"Number {n} is out of supported range [-999999999999, 999999999999]")
    
    # Special case for zero
    if n == 0:
        return "zero"
    
    # Handle negative numbers
    if n < 0:
        return "negative " + number_to_words(-n)
    
    # Word mappings
    ones = [
        "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    ]
    
    teens = [
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"
    ]
    
    tens = [
        "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
    ]
    
    scales = [
        (1000000000000, "trillion"),  # Not used in our range, but for completeness
        (1000000000, "billion"),
        (1000000, "million"),
        (1000, "thousand"),
        (1, "")
    ]
    
    def convert_hundreds(num):
        """Convert a number 0-999 to words."""
        result = []
        
        # Hundreds place
        hundreds_digit = num // 100
        if hundreds_digit > 0:
            result.append(ones[hundreds_digit])
            result.append("hundred")
        
        # Tens and ones place
        remainder = num % 100
        if remainder >= 20:
            tens_digit = remainder // 10
            ones_digit = remainder % 10
            if ones_digit > 0:
                result.append(tens[tens_digit] + "-" + ones[ones_digit])
            else:
                result.append(tens[tens_digit])
        elif remainder >= 10:
            result.append(teens[remainder - 10])
        elif remainder > 0:
            result.append(ones[remainder])
        
        return result
    
    # Process the number by scale groups
    parts = []
    
    for scale_value, scale_name in scales:
        if scale_value > n:
            continue
        
        group_value = n // scale_value
        n = n % scale_value
        
        if group_value == 0:
            continue
        
        # Convert the group (0-999)
        group_words = convert_hundreds(group_value)
        
        if scale_name:
            group_words.append(scale_name)
        
        parts.extend(group_words)
    
    return " ".join(parts)
