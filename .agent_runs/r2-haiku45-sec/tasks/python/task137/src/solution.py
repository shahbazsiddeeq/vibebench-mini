import tokenize
import io
from typing import List, Tuple


def find_markers(source: str) -> List[Tuple[int, str]]:
    """
    Find TODO and FIXME markers in Python comments.
    
    Returns a list of (1-based line number, marker) tuples for each line
    containing 'TODO' or 'FIXME' in a comment (case-sensitive).
    
    Only markers in actual comment tokens are reported, not in strings.
    If tokenization fails, only successfully tokenized comments are returned.
    Results are ordered by line number.
    """
    if not isinstance(source, str):
        return []
    
    results = []
    
    try:
        # Tokenize the source code
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        
        for token_type, token_string, start, end, line in tokens:
            # Only process comment tokens
            if token_type == tokenize.COMMENT:
                line_number = start[0]  # 1-based line number
                
                # Extract the comment text (remove the '#' prefix)
                comment_text = token_string[1:] if token_string.startswith('#') else token_string
                
                # Find which marker appears first in the comment
                todo_pos = comment_text.find('TODO')
                fixme_pos = comment_text.find('FIXME')
                
                # Determine which marker to report (if any)
                marker = None
                if todo_pos != -1 and fixme_pos != -1:
                    # Both present, use the one that appears first
                    if todo_pos < fixme_pos:
                        marker = 'TODO'
                    else:
                        marker = 'FIXME'
                elif todo_pos != -1:
                    marker = 'TODO'
                elif fixme_pos != -1:
                    marker = 'FIXME'
                
                if marker:
                    results.append((line_number, marker))
    
    except tokenize.TokenError:
        # Tokenization failed - return what we've collected so far
        pass
    
    return results
