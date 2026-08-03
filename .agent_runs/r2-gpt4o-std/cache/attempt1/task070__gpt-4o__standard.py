from html.parser import HTMLParser
from html import escape

class HTMLSanitizer(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.allowed_tags:
            self.result.append(f"<{tag.lower()}>")

    def handle_endtag(self, tag):
        if tag.lower() in self.allowed_tags:
            self.result.append(f"</{tag.lower()}>")

    def handle_data(self, data):
        self.result.append(escape(data))

    def handle_comment(self, data):
        pass  # Ignore comments

    def handle_decl(self, decl):
        pass  # Ignore declarations

    def get_sanitized_html(self):
        return ''.join(self.result)

def sanitize_html(html, allowed_tags):
    parser = HTMLSanitizer(allowed_tags)
    parser.feed(html)
    return parser.get_sanitized_html()
