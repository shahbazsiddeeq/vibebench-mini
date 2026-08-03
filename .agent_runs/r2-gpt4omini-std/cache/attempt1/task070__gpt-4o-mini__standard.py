# src/solution.py

from html.parser import HTMLParser
from html import escape

class Sanitizer(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.result = []
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.allowed_tags:
            self.result.append(f"<{tag.lower()}>")
        else:
            self.skip_content = True

    def handle_endtag(self, tag):
        if tag.lower() in self.allowed_tags:
            self.result.append(f"</{tag.lower()}>")

    def handle_data(self, data):
        if not self.skip_content:
            self.result.append(escape(data))

    def handle_comment(self, data):
        pass  # Ignore comments

    def handle_declaration(self, data):
        pass  # Ignore declarations

    def handle_entityref(self, name):
        pass  # Ignore entity references

    def handle_charref(self, name):
        pass  # Ignore character references

def sanitize_html(html, allowed_tags):
    sanitizer = Sanitizer(allowed_tags)
    sanitizer.feed(html)
    return ''.join(sanitizer.result)
