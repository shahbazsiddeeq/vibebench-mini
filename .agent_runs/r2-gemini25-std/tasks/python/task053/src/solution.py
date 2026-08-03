def count_lines(path: str) -> int:
    """
    Counts the number of lines in a UTF-8 text file.

    Args:
        path: The path to the text file.

    Returns:
        The number of lines in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            line_count = 0
            for _ in f:
                line_count += 1
            return line_count
    except FileNotFoundError:
        raise
    except Exception as e:
        # Catch other potential I/O errors and re-raise them
        raise IOError(f"An error occurred while reading the file: {e}") from e
