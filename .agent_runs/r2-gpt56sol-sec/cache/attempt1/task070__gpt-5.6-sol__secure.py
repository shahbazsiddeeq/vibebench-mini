from html import escape
from html.parser import HTMLParser
import re
from collections.abc import Iterable


_TAG_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9:_-]*\Z")


class _SanitizingParser(HTMLParser):
    def __init__(self, allowed_tags: frozenset[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.allowed_tags = allowed_tags
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.parts.append(f"<{tag}>")

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.parts.append(f"<{tag}>")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.allowed_tags:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(escape(data, quote=False))

    def handle_entityref(self, name: str) -> None:
        self.parts.append(escape(f"&{name};", quote=False))

    def handle_charref(self, name: str) -> None:
        self.parts.append(escape(f"&#{name};", quote=False))

    def handle_comment(self, data: str) -> None:
        pass

    def handle_decl(self, decl: str) -> None:
        pass

    def unknown_decl(self, data: str) -> None:
        pass

    def handle_pi(self, data: str) -> None:
        pass


def sanitize_html(html: str, allowed_tags: Iterable[str]) -> str:
    """Sanitize untrusted HTML using an allow-list of tag names."""
    if not isinstance(html, str):
        raise TypeError("html must be a string")
    if isinstance(allowed_tags, (str, bytes)) or not isinstance(
        allowed_tags, Iterable
    ):
        raise TypeError("allowed_tags must be an iterable of tag names")

    normalized: set[str] = set()
    try:
        for tag in allowed_tags:
            if not isinstance(tag, str):
                raise TypeError("allowed tag names must be strings")
            if not _TAG_NAME.fullmatch(tag):
                raise ValueError("allowed tag name is invalid")
            normalized.add(tag.lower())
    except (TypeError, ValueError):
        raise
    except Exception:
        raise ValueError("could not read allowed tag names") from None

    parser = _SanitizingParser(frozenset(normalized))
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        return escape(html, quote=False)

    return "".join(parser.parts)


__all__ = ["sanitize_html"]
