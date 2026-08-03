import unicodedata

def slugify(s: str) -> str:
    """
    Converts a string into a lowercased ASCII slug.

    Normalizes and strips accents from Latin characters, lowercases, then
    replaces runs of non-[a-z0-9] characters with a single hyphen.
    Leading/trailing hyphens are trimmed. Characters without ASCII representation
    (non-Latin scripts, emoji) are dropped. An empty string or a string with
    no slug-able characters returns "".

    Args:
        s: The input string.

    Returns:
        A lowercased ASCII slug.
    """
    if not isinstance(s, str):
        # For security and robustness, we only accept string inputs.
        # Any other type is considered invalid for this operation.
        return ""

    # Normalize to NFD (Normalization Form Canonical Decomposition)
    # and strip accents by filtering out non-spacing marks.
    normalized_s = unicodedata.normalize('NFD', s)
    stripped_accents = ''.join(
        char for char in normalized_s if not unicodedata.combining(char)
    )

    # Convert to lowercase
    lowercased_s = stripped_accents.lower()

    # Build the slug character by character
    slug_chars = []
    for char in lowercased_s:
        if 'a' <= char <= 'z' or '0' <= char <= '9':
            slug_chars.append(char)
        elif char.isspace() or char in '-_.,;!@#$%^&*()[]{}|\\/`~+=':
            # Replace various separators with a hyphen, but only if the last char wasn't already a hyphen
            if not slug_chars or slug_chars[-1] != '-':
                slug_chars.append('-')
        # Other characters (like non-Latin scripts, emoji) are dropped

    # Join characters and clean up hyphens
    result = "".join(slug_chars)

    # Trim leading and trailing hyphens
    result = result.strip('-')

    return result
