import tokenize
from io import StringIO

def find_markers(source):
    markers = []
    try:
        tokens = tokenize.generate_tokens(StringIO(source).readline)
        for token_type, token_string, start, _, _ in tokens:
            if token_type == tokenize.COMMENT:
                line_number = start[0]
                comment_text = token_string[1:].strip()  # Remove the '#' and strip whitespace
                if 'TODO' in comment_text:
                    markers.append((line_number, 'TODO'))
                elif 'FIXME' in comment_text:
                    markers.append((line_number, 'FIXME'))
    except tokenize.TokenError:
        pass
    return markers
