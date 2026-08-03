import base64
import json


def decode_jwt_header(token: str) -> dict:
    """
    Decode and return the header of a JWT token.
    
    The header is the first '.'-separated segment of the token, base64url-encoded.
    JWT segments omit base64 '=' padding, so padding must be re-added before decoding.
    
    Args:
        token: A JWT token string
        
    Returns:
        The decoded header as a dictionary
        
    Raises:
        ValueError: If the token has no '.', the segment is not valid base64url,
                   the content is not valid JSON, or the decoded JSON is not an object
    """
    # Validate input type
    if not isinstance(token, str):
        raise ValueError("Token must be a string")
    
    # Check for at least one '.' separator
    if '.' not in token:
        raise ValueError("Token must contain at least one '.' separator")
    
    # Extract the header segment (first part before the first '.')
    header_segment = token.split('.')[0]
    
    # Validate that header_segment is not empty
    if not header_segment:
        raise ValueError("Header segment cannot be empty")
    
    # Re-add padding to base64url-encoded segment
    # Base64 padding should make the length a multiple of 4
    padding_needed = (4 - len(header_segment) % 4) % 4
    padded_segment = header_segment + '=' * padding_needed
    
    # Decode from base64url
    try:
        header_bytes = base64.urlsafe_b64decode(padded_segment)
    except Exception as e:
        raise ValueError(f"Invalid base64url encoding: {e}")
    
    # Decode from bytes to string
    try:
        header_str = header_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Header is not valid UTF-8: {e}")
    
    # Parse JSON
    try:
        header_obj = json.loads(header_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Header is not valid JSON: {e}")
    
    # Validate that the decoded JSON is a dictionary (object)
    if not isinstance(header_obj, dict):
        raise ValueError("Decoded header must be a JSON object (dict), not a list, number, or string")
    
    return header_obj
