import collections

def tokenize(expr: str) -> list:
    """
    Splits an arithmetic expression string into a list of tokens.

    A number containing a '.' becomes a float, and a number without one
    becomes an int. Single-character operators and parentheses
    '+', '-', '*', '/', '(', ')', '^', '%' are emitted as str.
    Whitespace is ignored. Raises ValueError for any other character.

    Args:
        expr: The arithmetic expression string.

    Returns:
        A list of tokens.

    Raises:
        ValueError: If an invalid character is encountered.
    """
    if not isinstance(expr, str):
        raise TypeError("Input expression must be a string.")

    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        char = expr[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit():
            start = i
            is_float = False
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if is_float:  # Already encountered a dot
                        raise ValueError(f"Invalid number format at position {i}: multiple decimal points.")
                    is_float = True
                i += 1
            num_str = expr[start:i]
            try:
                if is_float:
                    tokens.append(float(num_str))
                else:
                    tokens.append(int(num_str))
            except ValueError:
                # This should ideally be caught by the parsing logic above,
                # but as a safeguard for edge cases like "1.2.3"
                raise ValueError(f"Invalid number format: '{num_str}'")
            continue

        if char in "+-*/()^%":
            tokens.append(char)
            i += 1
            continue

        raise ValueError(f"Invalid character '{char}' at position {i}")

    return tokens
