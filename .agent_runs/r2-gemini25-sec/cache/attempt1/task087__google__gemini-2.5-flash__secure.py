def parse_cookie(header: str) -> dict:
    """
    Parses a Cookie header string of the form "key=value; key2=value2" into a dict.

    Rules:
      - Split cookie pairs on ';'; split each pair on the FIRST '=' only, so a value may
        itself contain '=' (e.g. base64 values with '=' padding are preserved intact).
      - Surrounding whitespace around keys and values is trimmed.
      - Segments with no '=' are ignored.
      - For duplicate keys, the last value wins.

    Args:
        header: The Cookie header string.

    Returns:
        A dictionary representing the parsed cookies.
    """
    if not isinstance(header, str):
        # For security and robustness, only accept string input.
        # Raising a TypeError is appropriate for invalid input types.
        raise TypeError("Cookie header must be a string.")

    cookies = {}
    # Split the header into individual cookie pairs.
    # Using strip() on each segment to handle potential leading/trailing whitespace
    # around the semicolon.
    pairs = [pair.strip() for pair in header.split(';')]

    for pair in pairs:
        # Find the first occurrence of '='.
        # This ensures that values containing '=' are handled correctly.
        eq_index = pair.find('=')

        if eq_index == -1:
            # If no '=' is found, ignore the segment as per the rules.
            continue

        # Extract key and value based on the first '='.
        # Trim whitespace from key and value.
        key = pair[:eq_index].strip()
        value = pair[eq_index + 1:].strip()

        # If key is empty after stripping, ignore this pair.
        # This prevents cases like "=value" from creating an empty key.
        if not key:
            continue

        # Store the key-value pair.
        # For duplicate keys, the last value wins, which is naturally handled
        # by dictionary assignment.
        cookies[key] = value

    return cookies
