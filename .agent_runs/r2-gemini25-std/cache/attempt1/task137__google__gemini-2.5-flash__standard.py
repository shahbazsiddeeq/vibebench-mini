import tokenize
from io import BytesIO


def find_markers(source):
    """
    Scans Python source code for 'TODO' or 'FIXME' markers within comments.

    Args:
        source: A string containing Python source code.

    Returns:
        A list of tuples, where each tuple is (1-based line number, marker).
        Markers are 'TODO' or 'FIXME', case-sensitively.
        Only one marker is reported per line, the one appearing first in the comment.
        Results are ordered by line number.
    """
    markers = []
    try:
        # The tokenize module expects bytes, so encode the source.
        # Use 'utf-8' as a common encoding.
        source_bytes = source.encode('utf-8')
        # Use BytesIO to simulate a file for tokenize.generate_tokens
        readline = BytesIO(source_bytes).readline

        for token_info in tokenize.generate_tokens(readline):
            token_type, token_string, start, end, line_text = token_info

            if token_type == tokenize.COMMENT:
                line_num = start[0]
                comment_text = token_string

                todo_index = comment_text.find('TODO')
                fixme_index = comment_text.find('FIXME')

                if todo_index != -1 and (fixme_index == -1 or todo_index < fixme_index):
                    markers.append((line_num, 'TODO'))
                elif fixme_index != -1:
                    markers.append((line_num, 'FIXME'))

    except tokenize.TokenError:
        # If tokenization fails, return the markers found up to that point.
        # The problem description states: "If the source cannot be fully tokenized
        # ... the comments tokenized before the failure are still reported and
        # nothing else is - there is no raw text fallback."
        pass
    except Exception:
        # Catch any other unexpected exceptions during tokenization
        pass

    return markers
