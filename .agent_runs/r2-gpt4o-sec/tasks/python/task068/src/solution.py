import hmac
import unicodedata

def secure_compare(a: str, b: str) -> bool:
    """
    Compares two strings in constant time to prevent timing attacks.

    :param a: First string to compare.
    :param b: Second string to compare.
    :return: True if strings are equal, False otherwise.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        return False

    # Normalize strings to ensure consistent comparison
    a_normalized = unicodedata.normalize('NFC', a)
    b_normalized = unicodedata.normalize('NFC', b)

    try:
        return hmac.compare_digest(a_normalized, b_normalized)
    except TypeError:
        return False
