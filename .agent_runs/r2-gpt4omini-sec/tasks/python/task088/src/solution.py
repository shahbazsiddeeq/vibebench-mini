# src/solution.py

def parse_email_headers(raw: str) -> dict:
    headers = {}
    lines = raw.splitlines()
    current_header = None
    current_value = []

    for line in lines:
        # Stop parsing at the first blank line
        if not line.strip():
            break
        
        # Check if the line is a continuation of the previous header
        if line.startswith(' ') or line.startswith('\t'):
            if current_header is not None:
                # Strip leading/trailing whitespace and add to current value
                current_value.append(line.strip())
            continue
        
        # If we have a new header, save the previous one
        if current_header is not None:
            headers[current_header] = ' '.join(current_value)
        
        # Split the line into key and value
        try:
            key, value = line.split(':', 1)
        except ValueError:
            continue  # Skip malformed lines
        
        # Normalize the header key to Title-Case
        current_header = key.strip().title()
        current_value = [value.strip()]

    # Save the last header if it exists
    if current_header is not None:
        headers[current_header] = ' '.join(current_value)

    return headers
