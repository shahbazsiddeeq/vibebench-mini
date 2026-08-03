# src/solution.py

def parse_email_headers(raw: str) -> dict:
    headers = {}
    lines = raw.splitlines()
    current_header = None
    current_value = []

    for line in lines:
        stripped_line = line.strip()
        
        # Stop parsing at the first blank line
        if not stripped_line:
            break
        
        # Check if the line is a continuation of the previous header
        if stripped_line.startswith(' ') or stripped_line.startswith('\t'):
            if current_header is not None:
                current_value.append(stripped_line.strip())
            continue
        
        # If we have a new header, save the previous one
        if current_header is not None:
            headers[current_header] = ' '.join(current_value)
        
        # Split the line into key and value
        try:
            key, value = stripped_line.split(':', 1)
            current_header = key.strip().title()  # Normalize to Title-Case
            current_value = [value.strip()]  # Start a new value list
        except ValueError:
            # If the line doesn't contain a valid header, we ignore it
            continue

    # Save the last header if it exists
    if current_header is not None:
        headers[current_header] = ' '.join(current_value)

    return headers
