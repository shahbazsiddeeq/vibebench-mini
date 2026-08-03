import base64
import json

def decode_jwt_header(token: str) -> dict:
    # Validate input
    if not isinstance(token, str):
        raise ValueError("Token must be a string.")
    
    # Split the token into segments
    segments = token.split('.')
    if len(segments) < 1:
        raise ValueError("Token must contain at least one segment separated by '.'.")

    # Get the header segment
    header_segment = segments[0]

    # Calculate the necessary padding
    padding_needed = 4 - (len(header_segment) % 4)
    if padding_needed < 4:
        header_segment += '=' * padding_needed

    # Decode the base64url segment
    try:
        decoded_bytes = base64.urlsafe_b64decode(header_segment)
    except (ValueError, TypeError):
        raise ValueError("Invalid base64url encoding.")

    # Convert bytes to JSON
    try:
        header_json = json.loads(decoded_bytes)
    except json.JSONDecodeError:
        raise ValueError("Decoded content is not valid JSON.")

    # Ensure the decoded JSON is an object
    if not isinstance(header_json, dict):
        raise ValueError("Decoded JSON is not an object.")

    return header_json
