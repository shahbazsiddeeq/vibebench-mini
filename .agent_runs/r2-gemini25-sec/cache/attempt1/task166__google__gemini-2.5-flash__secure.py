import urllib.parse

def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parses a URL query string (WITHOUT any leading '?') into a dict mapping
    each decoded key to the ordered list of its decoded values.

    Args:
        qs: The URL query string to parse.

    Returns:
        A dictionary where keys are decoded query parameter names and values
        are lists of decoded query parameter values, in the order they appeared.
    """
    if not isinstance(qs, str):
        # While the type hint suggests str, robust code should handle non-string inputs
        # if there's any chance of them occurring. Here, we'll raise a TypeError
        # as per typical Python behavior for incorrect types.
        raise TypeError("Query string must be a string.")

    result: dict[str, list[str]] = {}

    if not qs:
        return result

    # Split the query string into segments by '&'
    segments = qs.split('&')

    for segment in segments:
        # Skip empty segments (e.g., from "&&" or trailing "&")
        if not segment:
            continue

        # Split each segment at the first '='
        parts = segment.split('=', 1)

        key_encoded: str
        value_encoded: str

        if len(parts) == 2:
            key_encoded = parts[0]
            value_encoded = parts[1]
        else:
            # Segment has no '=' (e.g., 'flag')
            key_encoded = parts[0]
            value_encoded = '' # Value is an empty string

        # Percent-decode key and value, and replace '+' with space
        # urllib.parse.unquote_plus handles malformed percent escapes by leaving them as-is.
        key = urllib.parse.unquote_plus(key_encoded)
        value = urllib.parse.unquote_plus(value_encoded)

        # Append the value to the list for the corresponding key
        if key not in result:
            result[key] = []
        result[key].append(value)

    return result
