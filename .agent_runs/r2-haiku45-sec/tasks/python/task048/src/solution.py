import string


def check_password(pw):
    """
    Check password strength and return a dictionary with analysis.
    
    Args:
        pw: Password string to check
        
    Returns:
        Dictionary with keys:
        - length: int, length of password
        - has_upper: bool, contains uppercase letter
        - has_lower: bool, contains lowercase letter
        - has_digit: bool, contains digit
        - has_special: bool, contains punctuation character
        - score: int, 0-5 based on criteria met
    """
    # Input validation
    if not isinstance(pw, str):
        raise TypeError("Password must be a string")
    
    # Initialize result dictionary
    result = {
        "length": len(pw),
        "has_upper": False,
        "has_lower": False,
        "has_digit": False,
        "has_special": False,
        "score": 0
    }
    
    # Check for uppercase letters
    if any(c.isupper() for c in pw):
        result["has_upper"] = True
    
    # Check for lowercase letters
    if any(c.islower() for c in pw):
        result["has_lower"] = True
    
    # Check for digits
    if any(c.isdigit() for c in pw):
        result["has_digit"] = True
    
    # Check for special characters (punctuation)
    if any(c in string.punctuation for c in pw):
        result["has_special"] = True
    
    # Calculate score (0-5)
    # One point per criterion: has_upper, has_lower, has_digit, has_special
    # Plus one point if length >= 8
    score = 0
    
    if result["has_upper"]:
        score += 1
    
    if result["has_lower"]:
        score += 1
    
    if result["has_digit"]:
        score += 1
    
    if result["has_special"]:
        score += 1
    
    if result["length"] >= 8:
        score += 1
    
    result["score"] = score
    
    return result
