def number_to_words(n: int) -> str:
    # Type checking - reject bool and non-int types
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    
    # Range checking
    if n < -999999999999 or n > 999999999999:
        raise ValueError("n must be in range [-999999999999, 999999999999]")
    
    # Special case for zero
    if n == 0:
        return "zero"
    
    # Handle negative numbers
    if n < 0:
        return "negative " + number_to_words(-n)
    
    # Words for numbers
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
             "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    scales = ["", "thousand", "million", "billion"]
    
    def convert_hundreds(num):
        """Convert a number 0-999 to words"""
        result = []
        
        # Hundreds place
        if num >= 100:
            result.append(ones[num // 100])
            result.append("hundred")
            num %= 100
        
        # Tens and ones place
        if num >= 20:
            tens_digit = num // 10
            ones_digit = num % 10
            if ones_digit == 0:
                result.append(tens[tens_digit])
            else:
                result.append(tens[tens_digit] + "-" + ones[ones_digit])
        elif num >= 10:
            result.append(teens[num - 10])
        elif num > 0:
            result.append(ones[num])
        
        return result
    
    # Break number into groups of three digits
    groups = []
    while n > 0:
        groups.append(n % 1000)
        n //= 1000
    
    # Convert each group and add scale words
    result = []
    for i in range(len(groups) - 1, -1, -1):
        if groups[i] > 0:
            group_words = convert_hundreds(groups[i])
            result.extend(group_words)
            if i > 0:
                result.append(scales[i])
    
    return " ".join(result)
