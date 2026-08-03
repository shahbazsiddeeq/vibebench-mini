from __future__ import annotations

_PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(s: str) -> bool:
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != _PAIRS[ch]:
                return False
            stack.pop()
    return len(stack) == 0
