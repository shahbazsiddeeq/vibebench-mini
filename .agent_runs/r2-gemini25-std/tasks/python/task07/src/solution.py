import re

def mask_email(s: str) -> str:
    """
    Finds email addresses in s and masks the username (the part before @),
    replacing it with its first character, then "***", then its last
    character (e.g. john.doe@example.com -> j***e@example.com). For a
    single-character username the same character is used as both first and last
    (a@x.io -> a***a@x.io). The domain (the part after @) is left unchanged,
    including its case, and addresses without a TLD such as user@localhost are
    masked too (user@localhost -> u***r@localhost). Text that is not part of an
    email address is left unchanged.
    """
    def replacer(match):
        username = match.group(1)
        domain = match.group(2)

        if not username:  # Should not happen with the current regex, but good for robustness
            return match.group(0)

        first_char = username[0]
        last_char = username[-1]

        masked_username = f"{first_char}***{last_char}"
        return f"{masked_username}@{domain}"

    # Regex to find email addresses.
    # It captures the username (before @) and the domain (after @).
    # The username can contain letters, numbers, and common special characters
    # like ._%+-
    # The domain can contain letters, numbers, hyphens, and dots.
    # It's a fairly broad regex to catch various valid email formats.
    email_pattern = r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9.-]+)"
    
    return re.sub(email_pattern, replacer, s)
