from html.parser import HTMLParser
import html

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
        self.result.append(html.escape(data))

    def handle_comment(self, data):
        pass  # Strip comments

    def handle_decl(self, decl):
        pass  # Strip declarations

    def handle_pi(self, data):
        pass  # Strip processing instructions

    def get_sanitized_html(self):
        return ''.join(self.result)

def sanitize_html(html_string, allowed_tags):
    try:
        sanitizer = HTMLSanitizer(allowed_tags)
        sanitizer.feed(html_string)
        sanitizer.close()
        return sanitizer.get_sanitized_html()
    except Exception:
        return ""  # In case of any parsing error, return an empty string
