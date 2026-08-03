# src/solution.py

def is_balanced(s: str) -> bool:
    # Validate input to ensure it's a string
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")

    # Define matching pairs
    matching_brackets = {')': '(', ']': '[', '}': '{'}
    open_brackets = set(matching_brackets.values())
    stack = []

    for char in s:
        if char in open_brackets:
            stack.append(char)
        elif char in matching_brackets:
            if not stack or stack[-1] != matching_brackets[char]:
                return False
            stack.pop()

    return len(stack) == 0
