def parse_email_headers(raw: str) -> dict:
    """
    Parses RFC 5322-style headers "Key: value" into a dict.

    Rules:
      - Header names are case-normalized to Title-Case (e.g. "content-type" -> "Content-Type").
      - Folded headers: a continuation line begins with whitespace (space or tab) and is
        part of the previous header's value. The unfolded value joins the parts with a
        single space, and leading/trailing whitespace on each part is stripped.
      - Parsing stops at the first blank line (the header/body separator); the body is ignored.
      - For duplicate header names, the last occurrence wins.

    Example: parse_email_headers("From: alice@x.com\nTo: bob@x.com") ->
      {"From": "alice@x.com", "To": "bob@x.com"}
    """
    headers = {}
    lines = raw.splitlines()
    
    current_header_name = None
    current_header_value_parts = []

    for line in lines:
        if not line.strip():  # Blank line indicates end of headers
            break

        if line[0].isspace():  # Folded header line
            if current_header_name:
                current_header_value_parts.append(line.strip())
            # If there's no current_header_name, this folded line is ignored
            # (e.g., if the input starts with a folded line)
        else:  # New header line
            if current_header_name:  # Store the previous header if it exists
                headers[current_header_name] = " ".join(current_header_value_parts)
            
            try:
                name, value = line.split(":", 1)
                current_header_name = _normalize_header_name(name.strip())
                current_header_value_parts = [value.strip()]
            except ValueError:
                # Malformed header line (e.g., no colon), treat as a new header
                # and potentially overwrite previous if name is empty or malformed.
                # For simplicity, we'll just skip it or treat it as a value part
                # if it was a folded line, but here it's a new line.
                # The spec implies a colon is required for a new header.
                # If no colon, it's not a valid header line.
                # We'll reset and effectively ignore this line as a header.
                current_header_name = None
                current_header_value_parts = []

    # Store the last header after the loop finishes
    if current_header_name:
        headers[current_header_name] = " ".join(current_header_value_parts)

    return headers

def _normalize_header_name(name: str) -> str:
    """
    Normalizes a header name to Title-Case.
    e.g., "content-type" -> "Content-Type"
    """
    return "-".join(word.capitalize() for word in name.split("-"))
