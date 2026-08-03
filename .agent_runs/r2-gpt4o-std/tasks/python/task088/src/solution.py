def parse_email_headers(raw):
    headers = {}
    current_key = None
    current_value = []

    for line in raw.splitlines():
        if not line.strip():
            break  # Stop at the first blank line

        if line[0] in ' \t' and current_key:
            # Continuation line
            current_value.append(line.strip())
        else:
            # New header line
            if current_key:
                # Save the previous header
                headers[current_key] = ' '.join(current_value).strip()

            # Split the new header line
            key, value = line.split(':', 1)
            current_key = key.strip().title()
            current_value = [value.strip()]

    if current_key:
        # Save the last header
        headers[current_key] = ' '.join(current_value).strip()

    return headers
