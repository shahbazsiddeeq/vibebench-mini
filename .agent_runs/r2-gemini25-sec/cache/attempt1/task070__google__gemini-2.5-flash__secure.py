import html
from html.parser import HTMLParser

class HTMLSanitizer(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        if not isinstance(allowed_tags, (list, tuple, set)):
            raise TypeError("allowed_tags must be a list, tuple, or set of strings.")
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.output = []
        self.in_allowed_tag = 0
        self.tag_stack = [] # To handle nested tags correctly

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            self.output.append(f"<{tag_lower}>")
            self.in_allowed_tag += 1
            self.tag_stack.append(tag_lower)
        else:
            # For disallowed tags, we still need to push something to the stack
            # to correctly handle nested disallowed tags and their content.
            self.tag_stack.append(None)

    def handle_endtag(self, tag):
        if not self.tag_stack:
            # Malformed HTML, end tag without a corresponding start tag.
            # We just ignore it.
            return

        # Pop the last tag from the stack
        popped_tag = self.tag_stack.pop()

        # If the popped tag was an allowed tag, and it matches the current end tag,
        # then we can close it.
        if popped_tag is not None and popped_tag == tag.lower():
            self.output.append(f"</{popped_tag}>")
            self.in_allowed_tag -= 1
        # If the popped tag was None (disallowed), or a mismatch,
        # we don't output anything. The in_allowed_tag counter only
        # decrements for actual allowed tags.

    def handle_data(self, data):
        # Only output data if we are inside an allowed tag, or if it's top-level text
        # and not inside a disallowed tag that we're currently skipping.
        # The `in_allowed_tag` counter ensures we only output text that is
        # part of an allowed element's content.
        # If `tag_stack` is empty, it's top-level text.
        # If `tag_stack` is not empty and the last element is None, it means
        # we are inside a disallowed tag, so we should not output data.
        if self.in_allowed_tag > 0 or (not self.tag_stack and data.strip()):
            self.output.append(html.escape(data))
        elif self.tag_stack and self.tag_stack[-1] is None:
            # We are inside a disallowed tag, so we don't output its content.
            pass
        else:
            # Top-level text that might be whitespace or other content not
            # explicitly inside an allowed tag. We still escape it.
            self.output.append(html.escape(data))


    def handle_entityref(self, name):
        # Convert entity references to their character equivalent if possible,
        # then escape them as data. This prevents things like &lt;script&gt;
        # from being reinterpreted as tags.
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        # Convert character references to their character equivalent if possible,
        # then escape them as data.
        self.handle_data(f"&#{name};")

    def handle_comment(self, data):
        pass  # Remove comments

    def handle_decl(self, decl):
        pass  # Remove declarations

    def handle_pi(self, data):
        pass  # Remove processing instructions

    def get_sanitized_html(self):
        return "".join(self.output)

def sanitize_html(html_string, allowed_tags):
    if not isinstance(html_string, str):
        raise TypeError("html_string must be a string.")
    if not isinstance(allowed_tags, (list, tuple, set)):
        raise TypeError("allowed_tags must be a list, tuple, or set of strings.")

    parser = HTMLSanitizer(allowed_tags)
    try:
        parser.feed(html_string)
        parser.close()
    except Exception:
        # Catch any parsing errors and return an empty string or re-raise
        # depending on desired error handling. For security, failing safe
        # by returning an empty string is often preferred.
        return ""
    return parser.get_sanitized_html()
