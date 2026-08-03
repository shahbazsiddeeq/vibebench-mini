# src/solution.py

def wildcard_match(pattern: str, text: str) -> bool:
    def match_helper(p_idx: int, t_idx: int) -> bool:
        if p_idx == len(pattern) and t_idx == len(text):
            return True
        if p_idx == len(pattern):
            return False
        if t_idx == len(text):
            return all(x == '*' for x in pattern[p_idx:])
        
        if pattern[p_idx] == '*':
            return match_helper(p_idx + 1, t_idx) or match_helper(p_idx, t_idx + 1)
        if pattern[p_idx] == '?' or pattern[p_idx] == text[t_idx]:
            return match_helper(p_idx + 1, t_idx + 1)
        
        return False

    return match_helper(0, 0)
