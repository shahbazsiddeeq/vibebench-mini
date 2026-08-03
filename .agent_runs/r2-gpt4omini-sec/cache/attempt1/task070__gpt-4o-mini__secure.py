# src/solution.py

from html.parser import HTMLParser
from html import escape

class HTMLSanitizer(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.result = []
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.result.append(f"<{tag}>")
        else:
            self.skip_content = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.result.append(f"</{tag}>")

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
    if not isinstance(html, str) or not isinstance(allowed_tags, list):
        raise ValueError("Invalid input types. 'html' must be a string and 'allowed_tags' must be a list.")
    
    sanitizer = HTMLSanitizer(allowed_tags)
    sanitizer.feed(html)
    return ''.join(sanitizer.result)
