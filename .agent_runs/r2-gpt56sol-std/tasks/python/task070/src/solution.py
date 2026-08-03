from html import escape
from html.parser import HTMLParser
from typing import Iterable


class _SanitizingParser(HTMLParser):
    _RAWTEXT_TAGS = {"script", "style"}

    def __init__(self, allowed_tags: set[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.allowed_tags = allowed_tags
        self.output: list[str] = []
        self._pending_raw_tag: str | None = None
        self._pending_raw_data: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()

        if tag in self.allowed_tags:
            self.output.append(f"<{tag}>")
        elif tag in self._RAWTEXT_TAGS:
            # Buffer disallowed raw-text content until a matching closing tag.
            # If the element is unterminated, close() will discard the buffer.
            self._pending_raw_tag = tag
            self._pending_raw_data = []

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.output.append(f"<{tag}>")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if self._pending_raw_tag == tag:
            self.output.extend(self._pending_raw_data)
            self._pending_raw_tag = None
            self._pending_raw_data = []

        if tag in self.allowed_tags:
            self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        escaped = escape(data, quote=False)
        if self._pending_raw_tag is not None:
            self._pending_raw_data.append(escaped)
        else:
            self.output.append(escaped)

    def handle_comment(self, data: str) -> None:
        pass

    def handle_decl(self, decl: str) -> None:
        pass

    def unknown_decl(self, data: str) -> None:
        pass

    def handle_pi(self, data: str) -> None:
        pass


def sanitize_html(html: str, allowed_tags: Iterable[str]) -> str:
    allowed = {tag.lower() for tag in allowed_tags}
    parser = _SanitizingParser(allowed)
    parser.feed(html)
    parser.close()
    return "".join(parser.output)
