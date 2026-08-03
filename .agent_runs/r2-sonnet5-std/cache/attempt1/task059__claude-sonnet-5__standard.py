import os


def tail(path, n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "r") as f:
        content = f.read()
    lines = content.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if n == 0:
        return []
    return lines[-n:]
