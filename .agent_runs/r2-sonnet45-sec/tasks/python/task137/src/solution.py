import io
import tokenize
from typing import List, Tuple


def find_markers(source: str) -> List[Tuple[int, str]]:
    """
    Find TODO/FIXME markers in Python source code comments.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of (line_number, marker) tuples, ordered by line number.
        Line numbers are 1-based.
    """
    if not isinstance(source, str):
        return []
    
    markers = []
    seen_lines = set()
    
    try:
        # Convert string to bytes for tokenization
        source_bytes = source.encode('utf-8')
        tokens = tokenize.tokenize(io.BytesIO(source_bytes).readline)
        
        for token in tokens:
            # Only process COMMENT tokens
            if token.type == tokenize.COMMENT:
                line_num = token.start[0]
                comment_text = token.string
                
                # Skip if we already found a marker on this line
                if line_num in seen_lines:
                    continue
                
                # Find positions of TODO and FIXME in the comment
                todo_pos = comment_text.find('TODO')
                fixme_pos = comment_text.find('FIXME')
                
                # Determine which marker appears first (if any)
                marker = None
                if todo_pos != -1 and fixme_pos != -1:
                    # Both present - use the one that appears first
                    marker = 'TODO' if todo_pos < fixme_pos else 'FIXME'
                elif todo_pos != -1:
                    marker = 'TODO'
                elif fixme_pos != -1:
                    marker = 'FIXME'
                
                if marker:
                    markers.append((line_num, marker))
                    seen_lines.add(line_num)
                    
    except tokenize.TokenError:
        # If tokenization fails, return what we found so far
        pass
    except Exception:
        # Handle any other unexpected errors gracefully
        pass
    
    # Sort by line number (should already be in order, but ensure it)
    markers.sort(key=lambda x: x[0])
    
    return markers
