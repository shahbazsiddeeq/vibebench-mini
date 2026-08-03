"""Quote-aware tokenizer for a single CSV record."""

from typing import List

__all__ = ["parse_csv_line"]


def parse_csv_line(line: str, delimiter: str = ",") -> List[str]:
    """Split one RFC4180-style CSV record into fields.

    Quoting is recognized only when a double quote is the first character of
    a field. Double quotes in unquoted fields are treated literally.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter == '"':
        raise ValueError('delimiter must be one character other than \'"\'') 

    fields: List[str] = []
    position = 0
    length = len(line)

    while True:
        if position == length:
            fields.append("")
            return fields

        if line[position] == '"':
            position += 1
            content: List[str] = []

            while True:
                if position >= length:
                    raise ValueError("unterminated quoted field")

                character = line[position]
                if character != '"':
                    content.append(character)
                    position += 1
                    continue

                if position + 1 < length and line[position + 1] == '"':
                    content.append('"')
                    position += 2
                    continue

                position += 1
                break

            fields.append("".join(content))

            if position == length:
                return fields
            if line[position] != delimiter:
                raise ValueError("unexpected character after closing quote")

            position += 1
            continue

        separator = line.find(delimiter, position)
        if separator == -1:
            fields.append(line[position:])
            return fields

        fields.append(line[position:separator])
        position = separator + 1
