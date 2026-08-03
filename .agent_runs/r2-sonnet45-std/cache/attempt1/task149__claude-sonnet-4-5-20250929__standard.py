def number_to_words(n: int) -> str:
    # Type check - reject non-int including bool
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer")
    
    # Range check
    if n < -999999999999 or n > 999999999999:
        raise ValueError("Number out of supported range")
    
    # Special case for zero
    if n == 0:
        return "zero"
    
    # Handle negative
    if n < 0:
        return "negative " + number_to_words(-n)
    
    # Define word mappings
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
             "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def convert_below_thousand(num):
        """Convert a number 0-999 to words"""
        if num == 0:
            return ""
        
        parts = []
        
        # Hundreds place
        hundreds_digit = num // 100
        if hundreds_digit > 0:
            parts.append(ones[hundreds_digit] + " hundred")
        
        # Tens and ones
        remainder = num % 100
        if remainder >= 20:
            tens_digit = remainder // 10
            ones_digit = remainder % 10
            if ones_digit > 0:
                parts.append(tens[tens_digit] + "-" + ones[ones_digit])
            else:
                parts.append(tens[tens_digit])
        elif remainder >= 10:
            parts.append(teens[remainder - 10])
        elif remainder > 0:
            parts.append(ones[remainder])
        
        return " ".join(parts)
    
    # Break number into groups of three
    billions = n // 1000000000
    millions = (n % 1000000000) // 1000000
    thousands = (n % 1000000) // 1000
    ones_group = n % 1000
    
    result_parts = []
    
    if billions > 0:
        result_parts.append(convert_below_thousand(billions) + " billion")
    
    if millions > 0:
        result_parts.append(convert_below_thousand(millions) + " million")
    
    if thousands > 0:
        result_parts.append(convert_below_thousand(thousands) + " thousand")
    
    if ones_group > 0:
        result_parts.append(convert_below_thousand(ones_group))
    
    return " ".join(result_parts)
