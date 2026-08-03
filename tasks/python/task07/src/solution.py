import re

EMAIL = re.compile(r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)")


def mask_email(s: str) -> str:
    def repl(m):
        user, dom = m.groups()
        return f"{user[0]}***{user[-1]}@{dom}"

    return EMAIL.sub(repl, s)
