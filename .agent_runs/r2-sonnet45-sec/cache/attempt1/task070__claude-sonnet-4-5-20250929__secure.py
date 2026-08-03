import html
from html.parser import HTMLParser
from typing import List, Set


class HTMLSanitizer(HTMLParser):
    """
    A secure HTML sanitizer that uses a real HTML parser to prevent XSS attacks.
    """
    
    def __init__(self, allowed_tags: Set[str]):
        super().__init__()
        # Store allowed tags in lowercase for case-insensitive comparison
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.output = []
        
    def handle_starttag(self, tag: str, attrs):
        """Handle opening tags - keep only if allowed, strip all attributes."""
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            # Emit the tag in lowercase with no attributes
            self.output.append(f"<{tag_lower}>")
    
    def handle_endtag(self, tag: str):
        """Handle closing tags - keep only if allowed."""
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            self.output.append(f"</{tag_lower}>")
    
    def handle_data(self, data: str):
        """Handle text content - escape it to prevent XSS."""
        # Escape &, <, > to prevent any markup from being interpreted
        escaped = html.escape(data, quote=False)
        self.output.append(escaped)
    
    def handle_comment(self, data: str):
        """Handle comments - remove them entirely."""
        pass
    
    def handle_decl(self, decl: str):
        """Handle declarations - remove them entirely."""
        pass
    
    def handle_pi(self, data: str):
        """Handle processing instructions - remove them entirely."""
        pass
    
    def handle_startendtag(self, tag: str, attrs):
        """Handle self-closing tags - keep only if allowed, strip all attributes."""
        tag_lower = tag.lower()
        if tag_lower in self.allowed_tags:
            # Emit as self-closing tag with no attributes
            self.output.append(f"<{tag_lower}>")
    
    def get_output(self) -> str:
        """Return the sanitized HTML."""
        return "".join(self.output)


def sanitize_html(html_string: str, allowed_tags: List[str]) -> str:
    """
    Sanitize an untrusted HTML string against an allow-list.
    
    Args:
        html_string: The HTML string to sanitize
        allowed_tags: List of tag names that are allowed (case-insensitive)
    
    Returns:
        Sanitized HTML string with only allowed tags (no attributes) and escaped text
    
    Security features:
    - Uses real HTML parser to handle malformed/adversarial input
    - Strips ALL attributes from allowed tags
    - Escapes text content to prevent XSS
    - Removes comments and declarations
    - Case-insensitive tag matching
    """
    # Input validation
    if not isinstance(html_string, str):
        raise TypeError("html_string must be a string")
    if not isinstance(allowed_tags, list):
        raise TypeError("allowed_tags must be a list")
    
    # Handle empty input
    if not html_string:
        return ""
    
    # Validate allowed_tags contains only strings
    for tag in allowed_tags:
        if not isinstance(tag, str):
            raise TypeError("All items in allowed_tags must be strings")
    
    # Create sanitizer with allowed tags
    allowed_set = set(allowed_tags)
    sanitizer = HTMLSanitizer(allowed_set)
    
    try:
        # Parse the HTML
        sanitizer.feed(html_string)
        sanitizer.close()
    except Exception:
        # If parsing fails, return empty string (fail secure)
        return ""
    
    return sanitizer.get_output()
