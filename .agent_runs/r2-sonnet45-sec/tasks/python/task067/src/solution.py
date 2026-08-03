import secrets
import base64


def gen_token(n_bytes=32):
    """
    Generate a URL-safe base64 token from cryptographically-secure random bytes.
    
    Args:
        n_bytes: Number of random bytes to generate (default: 32, minimum: 8)
        
    Returns:
        A URL-safe base64 encoded string without padding
        
    Raises:
        ValueError: If n_bytes < 8
    """
    # Validate input
    if not isinstance(n_bytes, int):
        raise ValueError("n_bytes must be an integer")
    
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode to URL-safe base64
    # urlsafe_b64encode uses '-' and '_' instead of '+' and '/'
    encoded = base64.urlsafe_b64encode(random_bytes)
    
    # Decode to string and strip padding
    token = encoded.decode('ascii').rstrip('=')
    
    return token
