def wildcard_match(pattern: str, text: str) -> bool:
    """
    Match a wildcard pattern against text.
    
    '*' matches zero or more characters.
    '?' matches exactly one character.
    All other characters must match exactly (case-sensitive).
    
    The match must cover the entire text (fully anchored).
    
    Args:
        pattern: The wildcard pattern string
        text: The text to match against
        
    Returns:
        True if pattern matches the entire text, False otherwise
    """
    # Validate inputs are strings
    if not isinstance(pattern, str) or not isinstance(text, str):
        return False
    
    # Use dynamic programming with memoization
    # dp[i][j] = True if pattern[0:i] matches text[0:j]
    memo = {}
    
    def matches(p_idx: int, t_idx: int) -> bool:
        """
        Check if pattern[p_idx:] matches text[t_idx:].
        
        Args:
            p_idx: Current index in pattern
            t_idx: Current index in text
            
        Returns:
            True if the remaining pattern matches the remaining text
        """
        # Check memo
        if (p_idx, t_idx) in memo:
            return memo[(p_idx, t_idx)]
        
        # Base cases
        if p_idx == len(pattern):
            # Pattern exhausted - match only if text is also exhausted
            result = t_idx == len(text)
        elif t_idx == len(text):
            # Text exhausted - pattern must be all stars
            result = all(c == '*' for c in pattern[p_idx:])
        else:
            # Both pattern and text have characters
            p_char = pattern[p_idx]
            
            if p_char == '*':
                # '*' can match zero or more characters
                # Try matching zero characters (skip the star)
                result = matches(p_idx + 1, t_idx)
                
                # If that didn't work, try matching one or more characters
                if not result:
                    result = matches(p_idx, t_idx + 1)
            elif p_char == '?':
                # '?' matches exactly one character
                result = matches(p_idx + 1, t_idx + 1)
            else:
                # Literal character - must match exactly
                result = p_char == text[t_idx] and matches(p_idx + 1, t_idx + 1)
        
        memo[(p_idx, t_idx)] = result
        return result
    
    return matches(0, 0)
