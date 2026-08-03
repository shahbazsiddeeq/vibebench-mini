import urllib.parse

def build_query(params: dict) -> str:
    """
    Builds a URL query string from a dictionary of parameters.

    List values become repeated keys. Keys are sorted alphabetically.
    Values are URL-encoded using application/x-www-form-urlencoded rules
    (spaces become '+').

    Args:
        params: A dictionary where keys are strings and values can be
                strings, numbers, or lists of strings/numbers.

    Returns:
        A URL query string.

    Raises:
        TypeError: If params is not a dictionary or if keys/values are of
                   unsupported types.
    """
    if not isinstance(params, dict):
        raise TypeError("Input 'params' must be a dictionary.")

    query_components = []
    sorted_keys = sorted(params.keys())

    for key in sorted_keys:
        if not isinstance(key, str):
            raise TypeError(f"Query parameter key must be a string, got {type(key).__name__}")

        value = params[key]

        if isinstance(value, list):
            # Handle list values: each item becomes a repeated key-value pair
            for item in value:
                # Ensure list items are convertible to string
                try:
                    encoded_item = urllib.parse.quote_plus(str(item))
                except Exception as e:
                    raise TypeError(f"Failed to encode list item '{item}': {e}")
                query_components.append(f"{urllib.parse.quote_plus(key)}={encoded_item}")
        else:
            # Handle single values (string, number, etc.)
            try:
                encoded_value = urllib.parse.quote_plus(str(value))
            except Exception as e:
                raise TypeError(f"Failed to encode value '{value}': {e}")
            query_components.append(f"{urllib.parse.quote_plus(key)}={encoded_value}")

    return "&".join(query_components)
