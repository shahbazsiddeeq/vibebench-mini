def is_balanced(s: str) -> bool:
    """
    Checks if all brackets ()[]{} in the input string are properly nested and matched.
    Non-bracket characters are ignored.

    Args:
        s: The input string to check.

    Returns:
        True if all brackets are balanced, False otherwise.
    """
    if not isinstance(s, str):
        # For security and robustness, validate input type.
        # Although the problem description implies string input,
        # explicit validation prevents unexpected behavior with other types.
        raise TypeError("Input must be a string.")

    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    opening_brackets = set(mapping.values())
    closing_brackets = set(mapping.keys())

    for char in s:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            if not stack:
                return False  # Closing bracket without a matching opening bracket
            top_of_stack = stack.pop()
            if mapping[char] != top_of_stack:
                return False  # Mismatched opening and closing brackets
        # Ignore non-bracket characters

    return not stack  # If the stack is empty, all brackets were matched
