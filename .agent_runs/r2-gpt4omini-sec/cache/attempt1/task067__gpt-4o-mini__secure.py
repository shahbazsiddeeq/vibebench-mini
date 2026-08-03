# src/solution.py

import secrets
import base64

def gen_token(n_bytes=32):
    if not isinstance(n_bytes, int) or n_bytes < 8:
        raise ValueError("n_bytes must be an integer greater than or equal to 8.")
    
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(n_bytes)
    
    # Encode the bytes to URL-safe base64
    token = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('utf-8')
    
    # Ensure the token has the correct length
    expected_length = (4 * n_bytes + 2) // 3
    if len(token) != expected_length:
        raise ValueError("Generated token does not have the expected length.")
    
    return token
