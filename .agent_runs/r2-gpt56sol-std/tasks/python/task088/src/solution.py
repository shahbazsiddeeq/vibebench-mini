"""Utilities for parsing RFC 5322-style email headers."""


def parse_email_headers(raw: str) -> dict[str, str]:
    """Parse email headers from *raw*, ignoring any message body."""
    headers: dict[str, str] = {}
    current_name: str | None = None
    current_parts: list[str] = []

    def commit() -> None:
        if current_name is not None:
            headers[current_name] = " ".join(current_parts)

    for line in raw.splitlines():
        if line == "":
            commit()
            return headers

        if line.startswith((" ", "\t")):
            if current_name is not None:
                current_parts.append(line.strip())
            continue

        commit()
        current_name = None
        current_parts = []

        if ":" not in line:
            continue

        name, value = line.split(":", 1)
        name = name.strip()
        if not name:
            continue

        current_name = name.title()
        current_parts = [value.strip()]

    commit()
    return headers
