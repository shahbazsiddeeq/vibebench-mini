import re


def mask_email(s):
    """
    Finds email addresses in s and masks the username part.
    
    The username (part before @) is replaced with:
    - first character + "***" + last character
    - For single-character usernames, the same character is used twice
    
    The domain (part after @) is left unchanged.
    
    Args:
        s: Input string that may contain email addresses
        
    Returns:
        String with email addresses masked
    """
    if not isinstance(s, str):
        return s
    
    # Email pattern that matches:
    # - username: one or more characters that are not whitespace or @
    # - @ symbol
    # - domain: one or more characters that are not whitespace
    # This handles both emails with TLDs (user@example.com) and without (user@localhost)
    email_pattern = r'\b([^\s@]+)@([^\s@]+)\b'
    
    def mask_username(match):
        username = match.group(1)
        domain = match.group(2)
        
        if len(username) == 0:
            # Edge case: empty username (shouldn't happen with our regex, but be safe)
            return match.group(0)
        elif len(username) == 1:
            # Single character: use it as both first and last
            masked_username = username[0] + "***" + username[0]
        else:
            # Multiple characters: first + *** + last
            masked_username = username[0] + "***" + username[-1]
        
        return masked_username + "@" + domain
    
    return re.sub(email_pattern, mask_username, s)
