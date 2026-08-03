import re


def mask_email(s: str) -> str:
    """
    Mask email addresses in a string by replacing the username part with
    first character + "***" + last character, while keeping the domain unchanged.
    
    Args:
        s: Input string that may contain email addresses
        
    Returns:
        String with email addresses masked
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Pattern to match email addresses
    # Username: one or more characters that are alphanumeric, dots, hyphens, underscores, plus signs
    # Domain: one or more characters that are alphanumeric, dots, hyphens
    email_pattern = r'([a-zA-Z0-9._+-]+)@([a-zA-Z0-9.-]+)'
    
    def mask_match(match):
        username = match.group(1)
        domain = match.group(2)
        
        # Mask the username: first char + "***" + last char
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        
        return f"{masked_username}@{domain}"
    
    # Replace all email addresses with masked versions
    result = re.sub(email_pattern, mask_match, s)
    
    return result
