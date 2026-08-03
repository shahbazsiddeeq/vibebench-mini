import secrets
import base64


def gen_token(n_bytes=32):
    """
    Generate a URL-safe base64 token from cryptographically-secure random bytes.
    
    Args:
        n_bytes: Number of random bytes to generate (must be >= 8)
        
    Returns:
        URL-safe base64 encoded token with padding stripped
        
    Raises:
        ValueError: if n_bytes < 8
    """
    # Input validation
    if not isinstance(n_bytes, int):
        raise ValueError("n_bytes must be an integer")
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    
    # Generate cryptographically-secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode to URL-safe base64 and strip padding
    token = base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')
    
    return token
