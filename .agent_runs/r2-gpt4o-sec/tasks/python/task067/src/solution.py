import secrets
import base64

def gen_token(n_bytes=32):
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode the bytes using URL-safe base64 encoding
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    
    # Strip any padding characters ('=')
    token = token.rstrip('=')
    
    # Ensure the token has the correct length
    expected_length = (4 * n_bytes + 2) // 3
    if len(token) != expected_length:
        raise RuntimeError("Generated token has incorrect length")
    
    return token
