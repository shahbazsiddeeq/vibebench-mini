import urllib.parse

def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parses a URL query string (WITHOUT any leading '?') into a dict mapping
    each decoded key to the ordered list of its decoded values.

    Pairs are separated by '&'; within a pair the key and value are split on
    the FIRST '=' only (so 'a=b=c' yields value 'b=c').
    A segment with no '=' (e.g. 'flag') becomes that key with the empty-string
    value ''. A segment like 'a=' yields the empty-string value ''.
    Empty segments produced by leading/trailing/doubled '&' (e.g. '&&' or a
    trailing '&') are skipped entirely.
    Both keys and values are percent-decoded and '+' is decoded to a space
    (application/x-www-form-urlencoded rules, via urllib.parse.unquote_plus).
    Repeated keys are NOT overwritten: every value is appended to that key's
    list in the order it appears. Keys are kept case-sensitive (verbatim after
    decoding).
    The empty string qs '' returns {}.
    Malformed percent escapes are left as-is by unquote_plus and never raise.

    Args:
        qs: The query string to parse.

    Returns:
        A dictionary where keys are decoded query parameter names and values
        are lists of their decoded values, in order of appearance.
    """
    if not qs:
        return {}

    result: dict[str, list[str]] = {}
    pairs = qs.split('&')

    for pair in pairs:
        if not pair:  # Skip empty segments
            continue

        if '=' in pair:
            key_encoded, value_encoded = pair.split('=', 1)
        else:
            key_encoded = pair
            value_encoded = ''

        key = urllib.parse.unquote_plus(key_encoded)
        value = urllib.parse.unquote_plus(value_encoded)

        if key not in result:
            result[key] = []
        result[key].append(value)

    return result
