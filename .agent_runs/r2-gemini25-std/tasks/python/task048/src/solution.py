import string

def check_password(pw):
    """
    Checks the strength of a password based on several criteria.

    Args:
        pw (str): The password string to check.

    Returns:
        dict: A dictionary containing the following keys:
            - 'length' (int): The length of the password.
            - 'has_upper' (bool): True if the password contains at least one uppercase letter, False otherwise.
            - 'has_lower' (bool): True if the password contains at least one lowercase letter, False otherwise.
            - 'has_digit' (bool): True if the password contains at least one digit, False otherwise.
            - 'has_special' (bool): True if the password contains at least one special character
                                     (from string.punctuation), False otherwise.
            - 'score' (int): A score from 0-5, where each satisfied criterion (including length >= 8)
                             adds one point.
    """
    length = len(pw)
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in string.punctuation for c in pw)

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
        "score": score,
    }
