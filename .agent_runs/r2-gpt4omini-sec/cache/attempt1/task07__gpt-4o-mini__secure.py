# src/solution.py

import re

def mask_email(s: str) -> str:
    """
    Masks email addresses in the given string by replacing the username part
    with its first character, followed by "***", and then its last character.
    
    Parameters:
    s (str): The input string potentially containing email addresses.
    
    Returns:
    str: The string with masked email addresses.
    """
    
    def mask(match):
        email = match.group(0)
        username, domain = email.split('@', 1)
        
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        
        return f"{masked_username}@{domain}"

    # Regular expression to find email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Substitute masked emails in the string
    return re.sub(email_pattern, mask, s)
