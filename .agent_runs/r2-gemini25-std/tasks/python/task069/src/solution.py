import base64
import json

def decode_jwt_header(token: str) -> dict:
    """
    Decodes and returns the header of a JWT token.

    Args:
        token: The JWT token string.

    Returns:
        A dictionary representing the decoded JWT header.

    Raises:
        ValueError: If the token has no '.', the segment is not valid base64url,
                    the content is not valid JSON, or the decoded JSON is not an object.
    """
    parts = token.split('.')
    if len(parts) < 1:
        raise ValueError("Invalid JWT token: no '.' separator found.")

    header_segment = parts[0]

    # Re-add padding for base64url decoding
    # Base64url padding is '=' characters to make the length a multiple of 4.
    # The number of '=' characters needed is (4 - (len % 4)) % 4.
    padding_needed = (4 - len(header_segment) % 4) % 4
    padded_header_segment = header_segment + '=' * padding_needed

    try:
        decoded_bytes = base64.urlsafe_b64decode(padded_header_segment)
    except Exception as e:
        raise ValueError(f"Invalid base64url encoding in header segment: {e}") from e

    try:
        decoded_json = json.loads(decoded_bytes.decode('utf-8'))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in decoded header: {e}") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 in decoded header: {e}") from e

    if not isinstance(decoded_json, dict):
        raise ValueError("Decoded header is not a JSON object.")

    return decoded_json
