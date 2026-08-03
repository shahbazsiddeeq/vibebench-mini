"""
src/solution.py

A simple, safe HTML sanitizer.

sanitize_html(html_str, allowed_tags) uses Python's built-in html.parser
(a real HTML tokenizer) instead of regular expressions to sanitize HTML
against an allow-list of tag names.

Rules implemented:
  * Tags whose (case-insensitive) name is in `allowed_tags` are kept, but
    emitted lower-cased with all attributes stripped.
  * All other tags are dropped entirely (only the tag markup is removed;
    any text between a disallowed tag's start and end tag is preserved
    as escaped text, unless the tag is a "raw text" element such as
    <script> or <style>, in which case an *unterminated* occurrence causes
    its trailing content to be dropped, matching how a real HTML parser
    behaves).
  * All text content is HTML-escaped (&, <, > become entities) so no
    leftover angle brackets can re-form executable markup.
  * Comments and declarations are removed.
"""

import html
from html.parser import HTMLParser


class _SanitizingParser(HTMLParser):
    def __init__(self, allowed_tags):
        # convert_charrefs=True makes text handling simpler/safer.
        super().__init__(convert_charrefs=True)
        self.allowed = {t.lower() for t in allowed_tags}
        self.out = []

    def _emit_start(self, tag):
        lowered = tag.lower()
        if lowered in self.allowed:
            self.out.append("<{}>".format(lowered))

    def _emit_end(self, tag):
        lowered = tag.lower()
        if lowered in self.allowed:
            self.out.append("</{}>".format(lowered))

    # --- HTMLParser callbacks -------------------------------------------------

    def handle_starttag(self, tag, attrs):
        self._emit_start(tag)

    def handle_startendtag(self, tag, attrs):
        # Self-closing tag like <br/> or <img/>
        self._emit_start(tag)

    def handle_endtag(self, tag):
        self._emit_end(tag)

    def handle_data(self, data):
        if data:
            self.out.append(html.escape(data, quote=False))

    def handle_comment(self, data):
        # Drop comments entirely.
        pass

    def handle_decl(self, decl):
        # Drop declarations (e.g. <!DOCTYPE ...>) entirely.
        pass

    def unknown_decl(self, data):
        # Drop unknown declarations / CDATA-like sections entirely.
        pass

    def handle_pi(self, data):
        # Drop processing instructions entirely.
        pass


def sanitize_html(html_str, allowed_tags):
    """
    Sanitize `html_str` against the allow-list `allowed_tags`.

    Returns a sanitized string where:
      - allowed tags survive (lower-cased, attribute-free),
      - disallowed tags are removed,
      - text is HTML-escaped so no markup can leak through.
    """
    if html_str is None:
        return ""

    parser = _SanitizingParser(allowed_tags)
    parser.feed(html_str)
    parser.close()
    return "".join(parser.out)
