import base64
import json


def decode_jwt_header(token):
    """
    Decode and return the header of a JWT token.
    
    Args:
        token: A JWT token string in format "header.payload.signature"
    
    Returns:
        dict: The decoded JWT header as a dictionary
    
    Raises:
        ValueError: If token format is invalid, base64 decoding fails,
                   JSON parsing fails, or decoded value is not an object
    """
    # Validate input type
    if not isinstance(token, str):
        raise ValueError("Token must be a string")
    
    # Check for at least one dot separator
    if '.' not in token:
        raise ValueError("Token must contain at least one '.' separator")
    
    # Extract the header segment (first part before '.')
    header_segment = token.split('.', 1)[0]
    
    # Validate the segment is not empty
    if not header_segment:
        raise ValueError("Header segment cannot be empty")
    
    # Add padding back to make length a multiple of 4
    # Base64 requires length to be multiple of 4
    padding_needed = (4 - len(header_segment) % 4) % 4
    padded_segment = header_segment + ('=' * padding_needed)
    
    # Decode from base64url
    try:
        decoded_bytes = base64.urlsafe_b64decode(padded_segment)
    except Exception as e:
        raise ValueError(f"Invalid base64url encoding in header segment") from e
    
    # Parse JSON
    try:
        decoded_json = json.loads(decoded_bytes)
    except json.JSONDecodeError as e:
        raise ValueError(f"Header segment does not contain valid JSON") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"Header segment contains invalid UTF-8") from e
    
    # Validate that the decoded JSON is an object (dict in Python)
    if not isinstance(decoded_json, dict):
        raise ValueError("Decoded JWT header must be a JSON object, not array/string/number/etc")
    
    return decoded_json
