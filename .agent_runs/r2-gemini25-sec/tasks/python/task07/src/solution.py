import re

def mask_email(s: str) -> str:
    """
    Finds email addresses in s and masks the username (the part before @),
    replacing it with its first character, then "***", then its last character.
    The domain (the part after @) is left unchanged.
    Text that is not part of an email address is left unchanged.

    Args:
        s: The input string potentially containing email addresses.

    Returns:
        The string with email usernames masked.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    # Regex to find email addresses.
    # This regex is designed to be reasonably robust for common email formats
    # but avoids being overly complex or permissive to prevent ReDoS or
    # matching non-email patterns.
    # It captures the username and the domain separately.
    # Username: [a-zA-Z0-9._%+-]+
    # Domain:   [a-zA-Z0-9.-]+\.[a-zA-Z]{2,} (for TLDs) OR [a-zA-Z0-9.-]+ (for localhost)
    # The overall pattern is designed to be non-greedy where appropriate.
    # We use a more general domain pattern to include 'localhost' and similar.
    # The username part allows common characters.
    # The domain part allows common characters and dots.
    # The final part after the last dot in the domain is not strictly enforced
    # to be a TLD, allowing for 'localhost' or internal domains.
    # This pattern is a balance between catching valid emails and avoiding
    # overly complex regex that might have security implications or performance issues.
    email_pattern = r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)"

    def _mask_match(match):
        username = match.group(1)
        domain = match.group(2)

        if not username:
            # This case should ideally not be hit with the current regex,
            # but as a defensive measure.
            return match.group(0)

        first_char = username[0]
        last_char = username[-1]

        # For single-character usernames, first and last are the same.
        # The problem statement implies this is handled correctly by the logic.
        # e.g., 'a' -> 'a***a'
        masked_username = f"{first_char}***{last_char}"
        return f"{masked_username}@{domain}"

    return re.sub(email_pattern, _mask_match, s)
