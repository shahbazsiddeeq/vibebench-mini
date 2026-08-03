def number_to_words(n: int) -> str:
    """
    Convert an integer to its English word representation.
    
    Args:
        n: An integer in the range [-999999999999, 999999999999]
        
    Returns:
        The English word representation of the number in lowercase
        
    Raises:
        TypeError: If n is not an int (including bool)
        ValueError: If n is outside the supported range
    """
    # Type validation - reject bool explicitly since bool is a subclass of int
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer")
    
    # Range validation
    if n < -999999999999 or n > 999999999999:
        raise ValueError("Number out of supported range")
    
    # Handle zero
    if n == 0:
        return "zero"
    
    # Handle negative numbers
    if n < 0:
        return "negative " + number_to_words(-n)
    
    # Define word mappings
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
    
    def convert_below_thousand(num):
        """Convert a number below 1000 to words."""
        if num == 0:
            return ""
        
        result = []
        
        # Handle hundreds
        hundreds_digit = num // 100
        if hundreds_digit > 0:
            result.append(ones[hundreds_digit])
            result.append("hundred")
        
        # Handle tens and ones
        remainder = num % 100
        if remainder >= 10 and remainder < 20:
            # Handle teens (10-19)
            result.append(teens[remainder - 10])
        else:
            tens_digit = remainder // 10
            ones_digit = remainder % 10
            
            if tens_digit > 0 and ones_digit > 0:
                # Hyphenate compound numbers like twenty-one
                result.append(tens[tens_digit] + "-" + ones[ones_digit])
            elif tens_digit > 0:
                result.append(tens[tens_digit])
            elif ones_digit > 0:
                result.append(ones[ones_digit])
        
        return " ".join(result)
    
    # Break number into groups of three digits
    billions = n // 1000000000
    millions = (n % 1000000000) // 1000000
    thousands = (n % 1000000) // 1000
    ones_group = n % 1000
    
    result = []
    
    # Process billions
    if billions > 0:
        result.append(convert_below_thousand(billions))
        result.append("billion")
    
    # Process millions
    if millions > 0:
        result.append(convert_below_thousand(millions))
        result.append("million")
    
    # Process thousands
    if thousands > 0:
        result.append(convert_below_thousand(thousands))
        result.append("thousand")
    
    # Process ones
    if ones_group > 0:
        result.append(convert_below_thousand(ones_group))
    
    return " ".join(result)
