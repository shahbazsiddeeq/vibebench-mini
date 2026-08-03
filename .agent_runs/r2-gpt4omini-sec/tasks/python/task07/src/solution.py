import re

def mask_email(s: str) -> str:
    def mask(match):
        email = match.group(0)
        username, domain = email.split('@', 1)
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        return f"{masked_username}@{domain}"

    # Regular expression to find email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|$)'
    
    # Substitute masked emails in the input string
    return re.sub(email_pattern, mask, s)
