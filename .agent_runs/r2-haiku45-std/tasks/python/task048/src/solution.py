import string

def check_password(pw):
    """
    Check password strength and return a dictionary with analysis.
    
    Returns:
        dict with keys:
            - length: int, length of password
            - has_upper: bool, contains uppercase letter
            - has_lower: bool, contains lowercase letter
            - has_digit: bool, contains digit
            - has_special: bool, contains special character (from string.punctuation)
            - score: int (0-5), one point per criterion where length>=8 counts as one
    """
    length = len(pw)
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in string.punctuation for c in pw)
    
    # Calculate score: one point per criterion
    score = 0
    if length >= 8:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1
    
    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "score": score
    }
