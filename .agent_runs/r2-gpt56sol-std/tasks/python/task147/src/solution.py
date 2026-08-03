def parse_csv_line(line: str, delimiter: str = ",") -> list[str]:
    """Split a single RFC4180-style CSV record into fields."""
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter == '"':
        raise ValueError('delimiter must be a single character other than \'"\'')
    if not isinstance(line, str):
        raise TypeError("line must be a string")

    fields: list[str] = []
    index = 0
    length = len(line)

    while True:
        if index < length and line[index] == '"':
            index += 1
            characters: list[str] = []

            while True:
                if index >= length:
                    raise ValueError("unterminated quoted field")

                character = line[index]
                if character != '"':
                    characters.append(character)
                    index += 1
                    continue

                if index + 1 < length and line[index + 1] == '"':
                    characters.append('"')
                    index += 2
                    continue

                index += 1
                break

            if index < length and line[index] != delimiter:
                raise ValueError("unexpected character after closing quote")

            fields.append("".join(characters))
        else:
            start = index
            while index < length and line[index] != delimiter:
                index += 1
            fields.append(line[start:index])

        if index == length:
            return fields

        index += 1
