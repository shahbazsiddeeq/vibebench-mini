import re

def mask_email(s: str) -> str:
    def mask(match):
        username = match.group(1)
        domain = match.group(2)
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        return f"{masked_username}@{domain}"

    email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|localhost)')
    return email_pattern.sub(mask, s)
