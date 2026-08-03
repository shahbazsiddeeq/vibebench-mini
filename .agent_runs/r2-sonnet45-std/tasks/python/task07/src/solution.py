import re

def mask_email(s):
    """
    Masks email addresses in a string by replacing the username part
    (before @) with first character + *** + last character.
    
    Args:
        s: String potentially containing email addresses
        
    Returns:
        String with masked email addresses
    """
    # Pattern to match email addresses
    # Username: one or more characters that are not whitespace or @
    # Domain: @ followed by one or more characters that are not whitespace
    email_pattern = r'\b([^\s@]+)@([^\s@]+)\b'
    
    def mask_username(match):
        username = match.group(1)
        domain = match.group(2)
        
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        
        return f"{masked_username}@{domain}"
    
    return re.sub(email_pattern, mask_username, s)
