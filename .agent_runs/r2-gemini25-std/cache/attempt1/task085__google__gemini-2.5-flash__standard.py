import urllib.parse

def build_query(params):
    """
    Builds a URL query string from a dictionary.

    - List values become repeated keys.
    - Keys are sorted alphabetically.
    - Values are URL-encoded (space encodes as '+').

    Args:
        params (dict): A dictionary where keys are strings and values can be
                       strings, numbers, or lists of strings/numbers.

    Returns:
        str: The URL query string.
    """
    if not params:
        return ""

    encoded_parts = []
    sorted_keys = sorted(params.keys())

    for key in sorted_keys:
        value = params[key]
        if isinstance(value, list):
            # For list values, create multiple key=value pairs
            for item in value:
                encoded_key = urllib.parse.quote(str(key), safe='')
                encoded_value = urllib.parse.quote_plus(str(item))
                encoded_parts.append(f"{encoded_key}={encoded_value}")
        else:
            # For single values, create a single key=value pair
            encoded_key = urllib.parse.quote(str(key), safe='')
            encoded_value = urllib.parse.quote_plus(str(value))
            encoded_parts.append(f"{encoded_key}={encoded_value}")

    return "&".join(encoded_parts)
