import os


def write_config(path, config):
    """
    Write an INI-style configuration file from a dict of section -> dict(key -> value).

    Each section is written as:
        [section]
        key=value
        (blank line)

    Sections are written in insertion order (dict order). Raises ValueError if
    any value contains a line break ('\n' or '\r'), or if the input types are
    not as expected.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")

    if not isinstance(config, dict):
        raise ValueError("config must be a dict")

    lines = []

    for section, pairs in config.items():
        if not isinstance(section, str):
            raise ValueError("section names must be strings")
        if '\n' in section or '\r' in section:
            raise ValueError("section names must not contain line breaks")
        if not isinstance(pairs, dict):
            raise ValueError("section values must be dicts of key->value")

        lines.append(f"[{section}]")

        for key, value in pairs.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("keys and values must be strings")
            if '\n' in key or '\r' in key:
                raise ValueError("keys must not contain line breaks")
            if '\n' in value or '\r' in value:
                raise ValueError("values must not contain line breaks")
            lines.append(f"{key}={value}")

        lines.append("")

    content = "\n".join(lines)
    if lines:
        content += "\n"

    dir_name = os.path.dirname(path)
    if dir_name and not os.path.isdir(dir_name):
        raise ValueError("invalid path: directory does not exist")

    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
    except OSError:
        raise ValueError("failed to write config file")
