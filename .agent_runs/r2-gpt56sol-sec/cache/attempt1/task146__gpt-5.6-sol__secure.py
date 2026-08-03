"""Fully anchored wildcard matching with '*' and '?' wildcards."""


def wildcard_match(pattern: str, text: str) -> bool:
    """Return whether *pattern* matches the entirety of *text*.

    ``*`` matches zero or more Unicode code points, while ``?`` matches
    exactly one. All other characters are matched literally and
    case-sensitively. Non-string inputs do not match.
    """
    if not isinstance(pattern, str) or not isinstance(text, str):
        return False

    pattern_index = 0
    text_index = 0
    last_star = -1
    star_text_index = -1

    while text_index < len(text):
        if (
            pattern_index < len(pattern)
            and pattern[pattern_index] != "*"
            and (
                pattern[pattern_index] == "?"
                or pattern[pattern_index] == text[text_index]
            )
        ):
            pattern_index += 1
            text_index += 1
        elif pattern_index < len(pattern) and pattern[pattern_index] == "*":
            last_star = pattern_index
            pattern_index += 1
            star_text_index = text_index
        elif last_star != -1:
            pattern_index = last_star + 1
            star_text_index += 1
            text_index = star_text_index
        else:
            return False

    while pattern_index < len(pattern) and pattern[pattern_index] == "*":
        pattern_index += 1

    return pattern_index == len(pattern)
