import re

_EMAIL_RE = re.compile(r'([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+)')


def mask_email(s: str) -> str:
    def _mask(match: re.Match) -> str:
        user, domain = match.group(1), match.group(2)
        first = user[0]
        last = user[-1]
        return f"{first}***{last}@{domain}"

    return _EMAIL_RE.sub(_mask, s)
