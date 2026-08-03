"""
CSV Line Tokenizer (Quote-Aware)

Implements parse_csv_line for splitting a single RFC4180-style CSV record
into fields, with support for quoted fields, escaped quotes, and custom
delimiters.
"""

from typing import List


def parse_csv_line(line: str, delimiter: str = ",") -> List[str]:
    """
    Parse a single CSV line into a list of fields.

    :param line: The raw CSV line to parse.
    :param delimiter: A single character used to separate fields.
    :raises ValueError: If delimiter is invalid, or the line contains
        malformed quoting (unterminated quote, or stray characters after
        a closing quote).
    :return: List of field strings.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")

    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise ValueError("delimiter must be a single character")

    if delimiter == '"':
        raise ValueError("delimiter cannot be the double-quote character")

    fields: List[str] = []
    n = len(line)
    i = 0

    while True:
        field_chars: List[str] = []

        if i < n and line[i] == '"':
            # Quoted field
            i += 1  # skip opening quote
            closed = False
            while i < n:
                ch = line[i]
                if ch == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field_chars.append('"')
                        i += 2
                        continue
                    else:
                        # closing quote
                        i += 1
                        closed = True
                        break
                else:
                    field_chars.append(ch)
                    i += 1

            if not closed:
                raise ValueError("Unterminated quoted field")

            # After closing quote, next char must be delimiter or end-of-line
            if i < n:
                if line[i] == delimiter:
                    fields.append("".join(field_chars))
                    i += 1
                    continue
                else:
                    raise ValueError(
                        "Unexpected characters after closing quote"
                    )
            else:
                fields.append("".join(field_chars))
                break
        else:
            # Unquoted field
            start = i
            while i < n and line[i] != delimiter:
                i += 1
            field_chars.append(line[start:i])
            fields.append("".join(field_chars))

            if i < n and line[i] == delimiter:
                i += 1
                continue
            else:
                break

    return fields
