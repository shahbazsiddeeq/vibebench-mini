import tokenize
from io import BytesIO


def find_markers(source):
    """
    Finds 'TODO' or 'FIXME' markers in Python comments.

    Args:
        source: A string containing Python source code.

    Returns:
        A list of tuples, where each tuple contains (1-based line number, marker).
        Markers are 'TODO' or 'FIXME', case-sensitively.
        At most one marker is reported per line, the one appearing first in the comment.
        Results are ordered by line number.
    """
    markers = []
    try:
        # The tokenize module expects bytes, so encode the source.
        # It also expects a file-like object, so use BytesIO.
        source_bytes = source.encode('utf-8')
        g = tokenize.tokenize(BytesIO(source_bytes).readline)

        for toktype, tokval, (srow, scol), (erow, ecol), line in g:
            if toktype == tokenize.COMMENT:
                # Check for 'TODO' first, then 'FIXME'
                if 'TODO' in tokval:
                    markers.append((srow, 'TODO'))
                elif 'FIXME' in tokval:
                    markers.append((srow, 'FIXME'))
    except tokenize.TokenError:
        # If tokenization fails, return markers found up to that point.
        pass

    # Ensure only one marker per line, prioritizing the first one found
    # and maintaining order by line number.
    unique_markers = {}
    for line_num, marker in markers:
        if line_num not in unique_markers:
            unique_markers[line_num] = marker
    
    # Sort by line number
    sorted_markers = sorted(unique_markers.items())
    
    return sorted_markers
