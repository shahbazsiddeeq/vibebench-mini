import re

EMAIL = re.compile(
    r"([A-Za-z0-9._%+-])([A-Za-z0-9._%+-]*)([A-Za-z0-9._%+-])@([A-Za-z0-9.-]+\.[A-Za-z]{2,})"
)


def mask_email(s: str) -> str:
    def repl(m):
        start, mid, end, dom = m.groups()
        return f"{start}***{end}@{dom}"

    return EMAIL.sub(repl, s)
