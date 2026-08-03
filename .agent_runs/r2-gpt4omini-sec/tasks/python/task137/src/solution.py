import ast
import re
from typing import List, Tuple

def find_markers(source: str) -> List[Tuple[int, str]]:
    markers = []
    line_number = 1
    source_lines = source.splitlines(keepends=True)
    
    for line in source_lines:
        # Strip the line to find comments
        stripped_line = line.strip()
        
        # Check for comments
        comment_match = re.search(r'#(.*)', stripped_line)
        if comment_match:
            comment_text = comment_match.group(1)
            # Check for TODO or FIXME in the comment
            if 'TODO' in comment_text:
                markers.append((line_number, 'TODO'))
            elif 'FIXME' in comment_text:
                markers.append((line_number, 'FIXME'))
        
        line_number += 1

    # Now we need to validate the source code to ensure it can be tokenized
    try:
        # Attempt to parse the source code to check for syntax errors
        ast.parse(source)
    except SyntaxError:
        # If there's a syntax error, we return the markers found before the error
        return markers

    return markers
