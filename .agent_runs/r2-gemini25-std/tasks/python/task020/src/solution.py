def is_balanced(s: str) -> bool:
    """
    Checks if all brackets ()[]{} in the string are properly nested and matched.
    Non-bracket characters are ignored.

    Args:
        s: The input string.

    Returns:
        True if all brackets are balanced, False otherwise.
    """
    stack = []
    bracket_map = {')': '(', ']': '[', '}': '{'}
    opening_brackets = set(bracket_map.values())
    closing_brackets = set(bracket_map.keys())

    for char in s:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            if not stack:
                return False  # Closing bracket without a corresponding opening bracket
            top_of_stack = stack.pop()
            if top_of_stack != bracket_map[char]:
                return False  # Mismatched opening and closing brackets

    return not stack  # True if stack is empty (all brackets matched), False otherwise
