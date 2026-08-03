import re

def mask_email(s: str) -> str:
    def mask(match):
        username = match.group(1)
        domain = match.group(2)
        if len(username) == 1:
            return f"{username}***{username}@{domain}"
        return f"{username[0]}***{username[-1]}@{domain}"

    email_pattern = r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})?)'
    return re.sub(email_pattern, mask, s)
