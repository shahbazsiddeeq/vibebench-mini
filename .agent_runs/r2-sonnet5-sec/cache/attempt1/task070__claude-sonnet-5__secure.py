"""
src/solution.py

A minimal, security-focused HTML sanitizer.

sanitize_html(html, allowed_tags) parses an untrusted HTML string with a real
HTML tokenizer (html.parser.HTMLParser) rather than regular expressions, so
that adversarial constructs (unterminated tags, attributes containing '>',
nested/re-emerging tag markers, comments, declarations, etc.) cannot be used
to smuggle live markup past the filter.

Rules implemented:
    * Only tags whose name (case-insensitively) is in `allowed_tags` are kept.
      Kept tags are re-emitted lower-cased with every attribute stripped.
    * All other tags are dropped entirely (only the tag markup itself is
      removed; any text content that the parser still delivers via its data
      handler is preserved, per the tokenizer's normal parsing rules).
    * Text content is HTML-escaped (&, <, >) so it can never re-form markup.
    * Comments, doctype/declarations, and processing instructions are removed.

This module uses only the Python standard library.
"""

from __future__ import annotations

import html
from html.parser import HTMLParser
from typing import Iterable, List


class _SanitizingParser(HTMLParser):
    """Internal HTMLParser subclass that builds a sanitized output string."""

    def __init__(self, allowed_tags: frozenset) -> None:
        # convert_charrefs=True (default) is fine: entities in text are
        # resolved to characters and then we re-escape them ourselves, which
        # keeps behavior consistent and prevents double-encoded bypasses.
        super().__init__(convert_charrefs=True)
        self._allowed_tags = allowed_tags
        self._out: List[str] = []

    # -- tag handling ---------------------------------------------------

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        self._emit_tag_if_allowed(tag, closing=False)

    def handle_endtag(self, tag: str) -> None:
        self._emit_tag_if_allowed(tag, closing=True)

    def handle_startendtag(self, tag: str, attrs) -> None:  # noqa: ANN001
        # Treat self-closing tags (e.g. <img ... />) as a simple start tag;
        # no matching end tag is required or emitted.
        self._emit_tag_if_allowed(tag, closing=False)

    def _emit_tag_if_allowed(self, tag: str, closing: bool) -> None:
        # HTMLParser already lower-cases tag names, but normalize defensively
        # in case of future/alternate parser behavior.
        name = (tag or "").lower()
        if name in self._allowed_tags:
            if closing:
                self._out.append(f"</{name}>")
            else:
                self._out.append(f"<{name}>")
        # Disallowed tags are simply dropped; no attributes ever survive.

    # -- data / text ------------------------------------------------------

    def handle_data(self, data: str) -> None:
        if data:
            self._out.append(html.escape(data, quote=False))

    def handle_entityref(self, name: str) -> None:
        # Only reached if convert_charrefs is False; kept for completeness.
        self.handle_data(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(html.unescape(f"&#{name};"))

    # -- things we intentionally strip -------------------------------------

    def handle_comment(self, data: str) -> None:
        # Comments are removed entirely, including any markup-looking text
        # inside them.
        return

    def handle_decl(self, decl: str) -> None:
        # <!DOCTYPE ...> and similar declarations are removed.
        return

    def unknown_decl(self, data: str) -> None:
        return

    def handle_pi(self, data: str) -> None:
        # Processing instructions (e.g. <?php ... ?>) are removed.
        return

    # -- result -------------------------------------------------------------

    def get_result(self) -> str:
        return "".join(self._out)


def sanitize_html(html_input: str, allowed_tags: Iterable[str]) -> str:
    """
    Sanitize an untrusted HTML string against an allow-list of tag names.

    Args:
        html_input: The raw, untrusted HTML string to sanitize.
        allowed_tags: An iterable of tag names (strings) that are permitted
            in the output. Comparison is case-insensitive; kept tags are
            emitted lower-cased with all attributes stripped.

    Returns:
        A sanitized string safe to embed as HTML text/markup, containing
        only the allowed tags (attribute-free) and HTML-escaped text.

    Raises:
        TypeError: If `html_input` is not a string, or `allowed_tags` is not
            an iterable of strings.
    """
    if not isinstance(html_input, str):
        raise TypeError("html_input must be a string")

    if isinstance(allowed_tags, (str, bytes)):
        # Guard against the common mistake of passing a single string
        # (which is iterable but not a collection of tag names).
        raise TypeError("allowed_tags must be an iterable of tag name strings")

    try:
        normalized_allowed = frozenset(
            str(tag).strip().lower()
            for tag in allowed_tags
            if isinstance(tag, str) and tag.strip()
        )
    except TypeError as exc:
        raise TypeError("allowed_tags must be an iterable of strings") from exc

    if html_input == "":
        return ""

    parser = _SanitizingParser(normalized_allowed)
    try:
        parser.feed(html_input)
        parser.close()
        return parser.get_result()
    except Exception:
        # Never leak parser internals/tracebacks to the caller; fail closed
        # by returning an empty (safe) result rather than raising or echoing
        # unsanitized content.
        return ""
