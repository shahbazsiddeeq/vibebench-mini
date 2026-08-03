import tokenize
import io
from typing import List, Tuple

def find_markers(source: str) -> List[Tuple[int, str]]:
    """
    Find TODO and FIXME markers in Python comments.
    
    Returns a list of (1-based line number, marker) tuples for each line
    containing 'TODO' or 'FIXME' in a comment (case-sensitive).
    
    Only actual comment tokens are scanned - text in strings is ignored.
    If tokenization fails, returns markers found before the failure.
    """
    results = []
    
    try:
        # Tokenize the source code
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        
        for token_type, token_string, start, end, line in tokens:
            # Only process comment tokens
            if token_type == tokenize.COMMENT:
                line_number = start[0]  # 1-based line number
                comment_text = token_string
                
                # Remove the '#' prefix to get the comment content
                if comment_text.startswith('#'):
                    comment_content = comment_text[1:]
                else:
                    comment_content = comment_text
                
                # Check for TODO or FIXME markers (case-sensitive)
                todo_pos = comment_content.find('TODO')
                fixme_pos = comment_content.find('FIXME')
                
                # Determine which marker appears first
                marker = None
                if todo_pos != -1 and fixme_pos != -1:
                    # Both present - use the one that appears first
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
        # Tokenization failed - return what we found so far
        pass
    
    return results
