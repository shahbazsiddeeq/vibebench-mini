import tokenize
import io


def find_markers(source):
    """
    Find TODO/FIXME markers in Python source code comments.
    
    Returns a list of (line_number, marker) tuples for lines containing
    TODO or FIXME in actual comment tokens (not in strings).
    """
    results = []
    
    try:
        # Convert string to bytes for tokenizer
        source_bytes = source.encode('utf-8')
        tokens = tokenize.tokenize(io.BytesIO(source_bytes).readline)
        
        for token in tokens:
            # Only process comment tokens
            if token.type == tokenize.COMMENT:
                comment_text = token.string
                line_number = token.start[0]
                
                # Find positions of TODO and FIXME in the comment
                todo_pos = comment_text.find('TODO')
                fixme_pos = comment_text.find('FIXME')
                
                # Determine which marker appears first (if any)
                marker = None
                if todo_pos != -1 and fixme_pos != -1:
                    # Both present, pick the one that appears first
                    marker = 'TODO' if todo_pos < fixme_pos else 'FIXME'
                elif todo_pos != -1:
                    marker = 'TODO'
                elif fixme_pos != -1:
                    marker = 'FIXME'
                
                if marker:
                    results.append((line_number, marker))
    
    except tokenize.TokenError:
        # If tokenization fails, return whatever we found so far
        pass
    
    return results
