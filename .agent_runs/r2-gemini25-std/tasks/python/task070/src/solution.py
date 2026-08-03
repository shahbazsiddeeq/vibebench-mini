import html.parser

class HTMLSanitizer(html.parser.HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.output = []
        self.in_allowed_tag = False

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            self.output.append(f"<{tag_lower}>")
            self.in_allowed_tag = True
        else:
            self.in_allowed_tag = False

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags and self.in_allowed_tag:
            self.output.append(f"</{tag_lower}>")
        self.in_allowed_tag = False # Reset in_allowed_tag state after an end tag

    def handle_data(self, data):
        # Always escape data, regardless of whether it's inside an allowed tag or not.
        # This prevents leftover angle brackets from re-forming executable markup.
        self.output.append(html.escape(data))

    def handle_comment(self, data):
        pass  # Drop comments

    def handle_decl(self, decl):
        pass  # Drop declarations

    def get_sanitized_html(self):
        return "".join(self.output)

def sanitize_html(html_string, allowed_tags):
    sanitizer = HTMLSanitizer(allowed_tags)
    sanitizer.feed(html_string)
    sanitizer.close()
    return sanitizer.get_sanitized_html()
