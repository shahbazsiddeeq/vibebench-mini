import re

def mask_email(s):
    """
    Finds email addresses in s and masks the username part.
    The username is replaced with: first_char + "***" + last_char
    The domain part is left unchanged.
    """
    def mask_match(match):
        email = match.group(0)
        # Split by @ to get username and domain
        parts = email.split('@')
        username = parts[0]
        domain = parts[1]
        
        # Mask the username
        if len(username) == 1:
            masked_username = username + "***" + username
        else:
            masked_username = username[0] + "***" + username[-1]
        
        return masked_username + "@" + domain
    
    # Pattern to match email addresses
    # Username can contain letters, digits, dots, hyphens, underscores
    # Domain can contain letters, digits, dots, hyphens
    pattern = r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+'
    
    return re.sub(pattern, mask_match, s)
