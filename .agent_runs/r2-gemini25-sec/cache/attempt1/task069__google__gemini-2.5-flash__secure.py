import json
import base64

def decode_jwt_header(token: str) -> dict:
    """
    Decodes and returns the header of a JWT token.

    The header is the first '.'-separated segment, base64url-encoded.
    JWT segments omit base64 '=' padding, so the decoder re-adds padding
    before decoding. The decoded header must be a JSON object.

    Args:
        token: The JWT token string.

    Returns:
        A dictionary representing the decoded JWT header.

    Raises:
        ValueError: If the token has no '.', the segment is not valid base64url,
                    the content is not valid JSON, or the decoded JSON is not
                    a dictionary (e.g., a list, number, or string).
    """
    if not isinstance(token, str):
        raise ValueError("Token must be a string.")

    parts = token.split('.')
    if len(parts) < 2:
        raise ValueError("Invalid JWT token: missing '.' separator.")

    header_segment = parts[0]

    # Re-add padding if necessary
    # Base64url padding ensures the length is a multiple of 4.
    # The number of '=' characters to add is (4 - (len % 4)) % 4.
    padding_needed = (4 - len(header_segment) % 4) % 4
    padded_header_segment = header_segment + '=' * padding_needed

    try:
        # Base64url decode
        decoded_bytes = base64.urlsafe_b64decode(padded_header_segment)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid base64url encoding in header segment: {e}") from e

    try:
        # Decode as UTF-8 string
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 encoding in decoded header: {e}") from e

    try:
        # Parse as JSON
        header_data = json.loads(decoded_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in header: {e}") from e

    if not isinstance(header_data, dict):
        raise ValueError("Decoded header is not a JSON object.")

    return header_data
