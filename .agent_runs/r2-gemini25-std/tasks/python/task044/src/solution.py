def to_snake(s: str) -> str:
    if not s:
        return ""

    result = []
    i = 0
    while i < len(s):
        if 'A' <= s[i] <= 'Z':
            # Find the end of the current uppercase run
            j = i
            while j < len(s) and 'A' <= s[j] <= 'Z':
                j += 1

            # If it's the first character and it's uppercase, or if there's a preceding character
            # and it's not an underscore, add an underscore.
            # This handles cases like "HTMLParser" -> "html_parser" and "parseHTML" -> "parse_html"
            if i > 0 and result and result[-1] != '_':
                result.append('_')

            # If the uppercase run is followed by a lowercase letter,
            # it means the last capital letter starts a new word.
            # E.g., "parseHTML" -> "parse_html" (H is part of HTML, but L starts a new word if it were "parseHTMLLower")
            # "HTMLParser" -> "html_parser" (P starts a new word)
            if j < len(s) and 'a' <= s[j] <= 'z':
                # If the run is longer than 1, split the last capital
                if j - i > 1:
                    result.append(s[i:j-1].lower())
                    result.append('_')
                    result.append(s[j-1].lower())
                else: # Run is just one capital letter
                    result.append(s[i].lower())
            else:
                # Entire run is uppercase or at the end of the string
                result.append(s[i:j].lower())
            i = j
        else:
            if i > 0 and 'A' <= s[i-1] <= 'Z' and 'a' <= s[i] <= 'z':
                # This condition is already handled by the uppercase block,
                # but as a safeguard, if a lowercase char follows an uppercase,
                # and we didn't add an underscore, add one.
                # This should ideally not be hit if the uppercase logic is correct.
                pass

            result.append(s[i])
            i += 1

    return "".join(result)


def to_camel(s: str) -> str:
    if not s:
        return ""

    parts = s.split('_')
    camel_parts = []

    for i, part in enumerate(parts):
        if not part:  # Handle consecutive underscores or leading/trailing underscores
            continue
        if i == 0:
            camel_parts.append(part.lower())
        else:
            camel_parts.append(part[0].upper() + part[1:].lower())

    return "".join(camel_parts)
