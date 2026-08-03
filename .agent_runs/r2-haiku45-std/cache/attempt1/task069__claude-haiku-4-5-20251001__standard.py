import base64
import json


def decode_jwt_header(token: str) -> dict:
    """
    Decode and return the header of a JWT token.
    
    The header is the first '.'-separated segment, base64url-encoded.
    JWT segments omit base64 '=' padding, so padding must be re-added before decoding.
    
    Args:
        token: A JWT token string
        
    Returns:
        The decoded header as a dict
        
    Raises:
        ValueError: If the token has no '.', the segment is not valid base64url,
                   the content is not valid JSON, or the decoded JSON is not an object
    """
    # Check if token contains a dot
    if '.' not in token:
        raise ValueError("Token must contain at least one '.' separator")
    
    # Extract the header segment (first part before the first dot)
    header_segment = token.split('.')[0]
    
    # Re-add padding if necessary
    # Base64 padding should make the length a multiple of 4
    padding_needed = len(header_segment) % 4
    if padding_needed:
        header_segment += '=' * (4 - padding_needed)
    
    # Decode from base64url
    try:
        header_bytes = base64.urlsafe_b64decode(header_segment)
    except Exception:
        raise ValueError("Invalid base64url encoding in header segment")
    
    # Parse JSON
    try:
        header = json.loads(header_bytes.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Header segment is not valid JSON")
    
    # Verify it's a dict (JSON object)
    if not isinstance(header, dict):
        raise ValueError("Decoded header must be a JSON object")
    
    return header
