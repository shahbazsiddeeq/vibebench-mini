import base64
import json

def decode_jwt_header(token: str) -> dict:
    # Split the token into segments
    segments = token.split('.')
    
    # Check if there are at least 2 segments (header and payload)
    if len(segments) < 2:
        raise ValueError("Token does not contain a valid header segment.")
    
    # Get the header segment
    header_segment = segments[0]
    
    # Calculate the required padding
    padding_needed = 4 - (len(header_segment) % 4)
    if padding_needed < 4:
        header_segment += '=' * padding_needed
    
    try:
        # Decode the base64url-encoded header
        decoded_bytes = base64.urlsafe_b64decode(header_segment)
    except (ValueError, TypeError):
        raise ValueError("Header segment is not valid base64url.")
    
    try:
        # Parse the JSON
        header_json = json.loads(decoded_bytes)
    except json.JSONDecodeError:
        raise ValueError("Decoded header is not valid JSON.")
    
    # Check if the result is a dictionary
    if not isinstance(header_json, dict):
        raise ValueError("Decoded JSON is not an object.")
    
    return header_json
