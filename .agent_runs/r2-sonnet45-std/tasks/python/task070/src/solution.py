from html.parser import HTMLParser
import html


class HTMLSanitizer(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = set(tag.lower() for tag in allowed_tags)
        self.result = []
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        self.tag_stack.append(tag_lower)
        if tag_lower in self.allowed_tags:
            self.result.append(f"<{tag_lower}>")
    
    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        # Pop from stack if it matches
        if self.tag_stack and self.tag_stack[-1] == tag_lower:
            self.tag_stack.pop()
        
        if tag_lower in self.allowed_tags:
            self.result.append(f"</{tag_lower}>")
    
    def handle_data(self, data):
        # Only include data if we're not inside a disallowed tag
        if not self.tag_stack or all(tag in self.allowed_tags for tag in self.tag_stack):
            # HTML-escape the data
            escaped = html.escape(data, quote=False)
            self.result.append(escaped)
    
    def handle_startendtag(self, tag, attrs):
        # Self-closing tags like <img />
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            self.result.append(f"<{tag_lower}>")
    
    def get_result(self):
        return ''.join(self.result)


def sanitize_html(html_string, allowed_tags):
    sanitizer = HTMLSanitizer(allowed_tags)
    sanitizer.feed(html_string)
    return sanitizer.get_result()
