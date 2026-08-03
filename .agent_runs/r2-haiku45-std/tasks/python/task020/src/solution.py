def is_balanced(s: str) -> bool:
    """
    Check if all brackets ()[]{}  are properly nested and matched.
    Non-bracket characters are ignored.
    
    Args:
        s: A string that may contain brackets and other characters
        
    Returns:
        True if all brackets are properly nested and matched, False otherwise
    """
    stack = []
    bracket_pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    opening_brackets = set('([{')
    closing_brackets = set(')]}')
    
    for char in s:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            stack.pop()
    
    return len(stack) == 0
