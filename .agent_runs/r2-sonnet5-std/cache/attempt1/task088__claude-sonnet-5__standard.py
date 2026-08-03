# src/solution.py

def parse_email_headers(raw):
    """
    Parse RFC 5322-style headers "Key: value" into a dict.
    """
    result = {}
    if not raw:
        return result

    lines = raw.split("\n")

    headers = []  # list of [name, value_parts]
    for line in lines:
        # Stop at first blank line
        if line.strip() == "":
            break

        if line and line[0] in (" ", "\t"):
            # continuation line
            if headers:
                headers[-1][1].append(line.strip())
            # if no previous header, ignore malformed continuation
            continue

        if ":" in line:
            name, _, value = line.partition(":")
            name = name.strip()
            value = value.strip()
            normalized_name = "-".join(
                part.capitalize() for part in name.split("-")
            )
            headers.append([normalized_name, [value]])
        # else: malformed line without colon, ignore

    for name, parts in headers:
        result[name] = " ".join(parts)

    return result
