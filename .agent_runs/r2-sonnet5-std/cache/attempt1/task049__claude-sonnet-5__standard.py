import re


def find_replace(text, replacements):
    if not replacements:
        return text

    keys = sorted(replacements.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(k) for k in keys))

    def repl(match):
        return replacements[match.group(0)]

    return pattern.sub(repl, text)
