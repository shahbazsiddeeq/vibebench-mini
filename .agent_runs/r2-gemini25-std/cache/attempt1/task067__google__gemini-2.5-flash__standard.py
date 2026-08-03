import secrets
import base64

def gen_token(n_bytes=32):
    """
    Generates a URL-safe base64 token encoding n_bytes of cryptographically-secure
    random bytes. The URL-safe alphabet is [A-Za-z0-9_-]; any base64 padding ('=')
    MUST be stripped.

    Args:
        n_bytes (int): The number of random bytes to generate. Must be at least 8.

    Returns:
        str: A URL-safe base64 encoded token string.

    Raises:
        ValueError: If n_bytes is less than 8.
    """
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8.")

    random_bytes = secrets.token_bytes(n_bytes)
    # base64.urlsafe_b64encode returns bytes, so decode to string
    # It also includes padding '=', which needs to be stripped
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
    return token
