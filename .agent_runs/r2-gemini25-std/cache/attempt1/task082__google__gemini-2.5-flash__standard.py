def write_config(path, config):
    """
    Writes an INI-style file from a dict of section->dict (of str keys to str values).
    Each section is written as a "[section]" header line followed by one "key=value"
    line per pair, then a blank line. Sections are written in insertion order.
    Raises ValueError if any value contains a line break (either '\n' or '\r').
    The file is UTF-8 encoded.
    """
    with open(path, 'w', encoding='utf-8') as f:
        for section_name, section_data in config.items():
            f.write(f"[{section_name}]\n")
            for key, value in section_data.items():
                if '\n' in value or '\r' in value:
                    raise ValueError("Value cannot contain line breaks ('\\n' or '\\r').")
                f.write(f"{key}={value}\n")
            f.write("\n")
