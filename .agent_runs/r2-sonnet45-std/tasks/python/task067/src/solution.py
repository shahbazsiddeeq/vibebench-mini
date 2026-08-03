import secrets
import base64


def gen_token(n_bytes=32):
    """
    Generate a URL-safe base64 token encoding n_bytes of cryptographically-secure random bytes.
    
    Args:
        n_bytes: Number of random bytes to encode (default: 32)
        
    Returns:
        A URL-safe base64 string without padding
        
    Raises:
        ValueError: If n_bytes < 8
    """
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode to URL-safe base64 and remove padding
    token = base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')
    
    return token
