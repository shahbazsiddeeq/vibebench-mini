from __future__ import annotations

from html import escape
from html.parser import HTMLParser


class _Sanitizer(HTMLParser):
    """Allow-list sanitizer built on a real HTML tokenizer.

    Tags whose name is in ``allowed`` are re-emitted with all attributes
    dropped; every other tag is discarded. All text data is HTML-escaped so
    that stray '<', '>' and '&' characters can never re-form markup that
    slipped past the tokenizer (e.g. via unterminated or nested tags).
    """

    def __init__(self, allowed: set[str]) -> None:
        # convert_charrefs=True feeds decoded text to handle_data, which we
        # then re-escape, normalizing entities safely.
        super().__init__(convert_charrefs=True)
        self.allowed = allowed
        self.out: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self.allowed:
            self.out.append(f"<{tag}>")

    def handle_startendtag(self, tag: str, attrs) -> None:
        if tag in self.allowed:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.allowed:
            self.out.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.out.append(escape(data, quote=False))

    # Comments, declarations, and processing instructions are dropped.
    def handle_comment(self, data: str) -> None:
        pass

    def handle_decl(self, decl: str) -> None:
        pass

    def handle_pi(self, data: str) -> None:
        pass

    def result(self) -> str:
        return "".join(self.out)


def sanitize_html(html: str, allowed_tags: list[str]) -> str:
    allowed = {t.lower() for t in allowed_tags}
    parser = _Sanitizer(allowed)
    parser.feed(html)
    parser.close()
    return parser.result()
