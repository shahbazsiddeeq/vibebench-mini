import string

def check_password(pw: str) -> dict:
    """
    Checks the strength of a given password based on several criteria.

    Args:
        pw: The password string to check.

    Returns:
        A dictionary containing:
        - 'length': The length of the password.
        - 'has_upper': True if the password contains at least one uppercase letter, False otherwise.
        - 'has_lower': True if the password contains at least one lowercase letter, False otherwise.
        - 'has_digit': True if the password contains at least one digit, False otherwise.
        - 'has_special': True if the password contains at least one special character
                         (from string.punctuation), False otherwise.
        - 'score': An integer score from 0 to 5, where each satisfied criterion
                   (including length >= 8) adds one point.
    """
    if not isinstance(pw, str):
        # For security, we should not expose internal error details.
        # A ValueError is appropriate for invalid input types.
        raise ValueError("Password must be a string.")

    length = len(pw)
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    score = 0

    # Iterate through the password once to check all character types
    for char in pw:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in string.punctuation:
            has_special = True

    # Calculate score based on criteria
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
        "score": score,
    }
