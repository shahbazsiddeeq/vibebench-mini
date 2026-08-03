from html.parser import HTMLParser
from html import escape


def sanitize_html(html, allowed_tags):
    """
    Sanitizes an untrusted HTML string against an allow-list.
    
    Rules:
    - A tag is kept only if its name (case-insensitive) is in allowed_tags;
      kept tags are emitted lowercased with ALL attributes removed.
    - Every other tag is dropped entirely.
    - Text content is preserved but HTML-escaped.
    - Comments and declarations are removed.
    """
    allowed_tags_lower = {tag.lower() for tag in allowed_tags}
    result = []
    
    class SanitizingParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            tag_lower = tag.lower()
            if tag_lower in allowed_tags_lower:
                result.append(f"<{tag_lower}>")
        
        def handle_endtag(self, tag):
            tag_lower = tag.lower()
            if tag_lower in allowed_tags_lower:
                result.append(f"</{tag_lower}>")
        
        def handle_data(self, data):
            # HTML-escape text content: &, <, > become entities
            result.append(escape(data))
        
        def handle_comment(self, data):
            # Remove comments
            pass
        
        def handle_decl(self, decl):
            # Remove declarations
            pass
        
        def handle_entityref(self, name):
            # Preserve entity references
            result.append(f"&{name};")
        
        def handle_charref(self, name):
            # Preserve character references
            result.append(f"&#{name};")
    
    parser = SanitizingParser()
    try:
        parser.feed(html)
    except Exception:
        # If parsing fails, return what we have so far
        pass
    
    return "".join(result)
