# src/solution.py

def parse_email_headers(raw: str) -> dict:
    headers = {}
    lines = raw.splitlines()
    current_header = None
    current_value = []

    for line in lines:
        # Check for blank line to stop parsing headers
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
            # Join the current value parts with a single space
            headers[current_header] = ' '.join(current_value)
        
        # Split the line into key and value
        key, value = line.split(':', 1)
        current_header = key.strip().title()  # Normalize header name to Title-Case
        current_value = [value.strip()]  # Start new value list

    # Save the last header if it exists
    if current_header is not None:
        headers[current_header] = ' '.join(current_value)

    return headers
