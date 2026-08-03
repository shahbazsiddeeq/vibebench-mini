import html
from html.parser import HTMLParser
from typing import List


def sanitize_html(html_string: str, allowed_tags: List[str]) -> str:
    """
    Sanitizes an untrusted HTML string against an allow-list of tags.
    
    Rules:
    - Only tags in allowed_tags (case-insensitive) are kept, lowercased, with all attributes removed
    - All other tags are dropped
    - Text content is HTML-escaped
    - Comments and declarations are removed
    
    Args:
        html_string: The untrusted HTML string to sanitize
        allowed_tags: List of allowed tag names (case-insensitive)
    
    Returns:
        Sanitized HTML string
    """
    if not html_string:
        return ""
    
    # Normalize allowed tags to lowercase for case-insensitive comparison
    allowed_tags_lower = {tag.lower() for tag in allowed_tags} if allowed_tags else set()
    
    class SanitizingParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []
        
        def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
            """Handle opening tags."""
            tag_lower = tag.lower()
            if tag_lower in allowed_tags_lower:
                # Keep the tag but strip all attributes
                self.result.append(f"<{tag_lower}>")
            # If tag is not allowed, it's silently dropped (not added to result)
        
        def handle_endtag(self, tag: str) -> None:
            """Handle closing tags."""
            tag_lower = tag.lower()
            if tag_lower in allowed_tags_lower:
                # Keep the closing tag
                self.result.append(f"</{tag_lower}>")
            # If tag is not allowed, it's silently dropped
        
        def handle_data(self, data: str) -> None:
            """Handle text content - escape it to prevent XSS."""
            # Use html.escape to convert &, <, > to entities
            escaped_data = html.escape(data, quote=False)
            self.result.append(escaped_data)
        
        def handle_comment(self, data: str) -> None:
            """Handle comments - remove them."""
            pass
        
        def handle_decl(self, decl: str) -> None:
            """Handle declarations - remove them."""
            pass
        
        def handle_pi(self, data: str) -> None:
            """Handle processing instructions - remove them."""
            pass
        
        def get_result(self) -> str:
            """Return the sanitized HTML."""
            return "".join(self.result)
    
    parser = SanitizingParser()
    try:
        parser.feed(html_string)
    except Exception:
        # If parsing fails, return empty string for safety
        return ""
    
    return parser.get_result()
