import re

def mask_email(s):
    def mask(match):
        username = match.group(1)
        domain = match.group(2)
        if len(username) == 1:
            masked_username = f"{username}***{username}"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        return f"{masked_username}@{domain}"

    email_pattern = r'(\b[\w.-]+)@([\w.-]+\b)'
    return re.sub(email_pattern, mask, s)
