import secrets
import base64

def gen_token(n_bytes=32):
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode the bytes to base64
    token = base64.urlsafe_b64encode(random_bytes)
    
    # Decode to string and strip padding
    token_str = token.decode('utf-8').rstrip('=')
    
    return token_str
