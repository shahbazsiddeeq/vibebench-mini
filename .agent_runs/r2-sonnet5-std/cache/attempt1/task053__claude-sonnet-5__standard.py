def count_lines(path):
    """Return the number of lines in a UTF-8 text file.

    Raises FileNotFoundError if the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)
