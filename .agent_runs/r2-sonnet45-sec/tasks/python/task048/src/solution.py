import string

def check_password(pw):
    """
    Analyzes password strength and returns a dictionary with criteria and score.
    
    Args:
        pw: Password string to check
        
    Returns:
        dict with keys: length, has_upper, has_lower, has_digit, has_special, score
    """
    # Validate input
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
    
    # Check each character for criteria
    for char in pw:
        if char.isupper():
            result["has_upper"] = True
        if char.islower():
            result["has_lower"] = True
        if char.isdigit():
            result["has_digit"] = True
        if char in string.punctuation:
            result["has_special"] = True
    
    # Calculate score (one point per satisfied criterion)
    score = 0
    
    # Length criterion: >= 8 characters
    if result["length"] >= 8:
        score += 1
    
    # Other criteria
    if result["has_upper"]:
        score += 1
    if result["has_lower"]:
        score += 1
    if result["has_digit"]:
        score += 1
    if result["has_special"]:
        score += 1
    
    result["score"] = score
    
    return result
