import tokenize
from io import BytesIO

def find_markers(source: str) -> list[tuple[int, str]]:
    """
    Scans Python source code for 'TODO' or 'FIXME' markers within comments.

    Args:
        source: A string containing the Python source code.

    Returns:
        A list of tuples, where each tuple contains the 1-based line number
        and the marker ('TODO' or 'FIXME') found on that line.
        Results are ordered by line number. At most one marker is reported
        per line, with 'TODO' taking precedence if both are present.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    markers = []
    source_bytes = source.encode('utf-8')
    try:
        g = tokenize.tokenize(BytesIO(source_bytes).readline)
        for toktype, tokval, (srow, scol), (erow, ecol), line in g:
            if toktype == tokenize.COMMENT:
                # Check for 'TODO' first
                if 'TODO' in tokval:
                    markers.append((srow, 'TODO'))
                # If 'TODO' not found, check for 'FIXME'
                elif 'FIXME' in tokval:
                    markers.append((srow, 'FIXME'))
            # If an unclosed bracket or string causes a TokenError,
            # we stop processing and return what we have so far.
            # The tokenize module handles this by raising an exception.
            # We don't need to explicitly catch it here as the loop
            # will simply terminate.
    except tokenize.TokenError:
        # If tokenization fails, return the markers found up to that point.
        # The problem description states: "If the source cannot be fully
        # tokenized ... the comments tokenized before the failure are still
        # reported and nothing else is". Our current loop structure naturally
        # handles this by stopping iteration on error.
        pass
    except Exception:
        # Catch any other unexpected errors during tokenization
        # and return an empty list or re-raise if specific error handling is needed.
        # For this problem, an empty list on unexpected error seems appropriate
        # as we don't want to expose internal details.
        return []

    # Deduplicate markers per line, prioritizing 'TODO' if both exist.
    # Since we append 'TODO' first, and then 'FIXME', the first occurrence
    # for a given line number will be the one we want to keep.
    unique_markers = {}
    for line_num, marker in markers:
        if line_num not in unique_markers:
            unique_markers[line_num] = marker
        elif marker == 'TODO' and unique_markers[line_num] == 'FIXME':
            # If 'TODO' is found later on the same line where 'FIXME' was
            # already recorded, update to 'TODO' as it has precedence.
            unique_markers[line_num] = 'TODO'

    # Sort by line number and convert back to list of tuples
    sorted_results = sorted(unique_markers.items())
    return list(sorted_results)
