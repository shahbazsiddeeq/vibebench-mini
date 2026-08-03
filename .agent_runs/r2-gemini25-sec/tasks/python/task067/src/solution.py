import secrets
import base64

def gen_token(n_bytes: int = 32) -> str:
    """
    Generates a URL-safe base64 token encoding n_bytes of cryptographically-secure
    random bytes.

    The URL-safe alphabet is [A-Za-z0-9_-]; any base64 padding ('=') MUST be
    stripped.

    Args:
        n_bytes: The number of random bytes to generate. Must be at least 8.

    Returns:
        A URL-safe base64 encoded string token.

    Raises:
        ValueError: If n_bytes is less than 8.
    """
    if not isinstance(n_bytes, int):
        raise TypeError("n_bytes must be an integer.")
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8.")

    random_bytes = secrets.token_bytes(n_bytes)
    # base64.urlsafe_b64encode returns bytes, so decode to string
    # .rstrip(b'=') removes any padding characters
    token = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('ascii')
    return token
