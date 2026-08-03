def parse_email_headers(raw):
    import re

    headers = {}
    current_key = None
    current_value_parts = []

    lines = raw.splitlines()
    for line in lines:
        if not line.strip():
            break  # Stop at the first blank line

        if line.startswith((' ', '\t')) and current_key:
            # Continuation line
            current_value_parts.append(line.strip())
        else:
            # New header line
            if current_key:
                # Store the previous header
                headers[current_key] = ' '.join(current_value_parts).strip()

            # Parse the new header
            match = re.match(r'^([^:]+):\s*(.*)$', line)
            if match:
                current_key = match.group(1).strip().title()
                current_value_parts = [match.group(2).strip()]

    if current_key:
        # Store the last header
        headers[current_key] = ' '.join(current_value_parts).strip()

    return headers
