"""
src/solution.py

A small, secure, self-contained MIME type guesser based on file extensions.

Design goals:
- No use of eval/exec.
- No filesystem or network I/O.
- Defensive input validation with safe fallbacks.
- Case-insensitive extension matching.
- Uses the last extension in multi-dotted filenames (e.g. "a.backup.png" -> .png).
"""

from typing import Final

# Fallback MIME type for unknown or unrecognized extensions.
_DEFAULT_MIME: Final[str] = "application/octet-stream"

# Mapping of lowercase file extensions (without leading dot) to MIME types.
_MIME_MAP: Final[dict] = {
    # Text
    "txt": "text/plain",
    "html": "text/html",
    "htm": "text/html",
    "css": "text/css",
    "csv": "text/csv",
    "xml": "text/xml",
    "md": "text/markdown",

    # Application
    "json": "application/json",
    "pdf": "application/pdf",
    "js": "application/javascript",
    "zip": "application/zip",
    "gz": "application/gzip",
    "tar": "application/x-tar",
    "doc": "application/msword",
    "xls": "application/vnd.ms-excel",
    "ppt": "application/vnd.ms-powerpoint",
    "bin": "application/octet-stream",

    # Images
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "svg": "image/svg+xml",
    "webp": "image/webp",
    "ico": "image/x-icon",

    # Audio
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",

    # Video
    "mp4": "video/mp4",
    "avi": "video/x-msvideo",
    "mov": "video/quicktime",
    "webm": "video/webm",
}


def guess_mime(filename: object) -> str:
    """
    Guess the MIME type of a file based on its extension.

    Parameters
    ----------
    filename : object
        The filename to inspect. Expected to be a string, but this function
        is defensive against unexpected types and malformed input.

    Returns
    -------
    str
        The guessed MIME type, or "application/octet-stream" if the type
        cannot be determined or the input is invalid.
    """
    # Validate input type strictly; never attempt eval/exec or dynamic code.
    if not isinstance(filename, str):
        return _DEFAULT_MIME

    # Guard against excessively long input to avoid potential resource abuse.
    if len(filename) == 0 or len(filename) > 4096:
        return _DEFAULT_MIME

    # Strip any surrounding whitespace defensively (does not affect logic
    # correctness for typical filenames, but avoids odd trailing spaces).
    name = filename.strip()
    if not name:
        return _DEFAULT_MIME

    # Only consider the final path component-like segment to avoid
    # accidental data leakage or confusion from path separators.
    # (No filesystem access performed here.)
    name = name.replace("\\", "/").rsplit("/", 1)[-1]

    # No dot means no extension -> fallback.
    if "." not in name:
        return _DEFAULT_MIME

    # Use the last extension segment, ignoring leading dots (hidden files).
    parts = name.split(".")
    ext = parts[-1].strip().lower()

    # Guard against empty extension (e.g. filename ending in a dot).
    if not ext:
        return _DEFAULT_MIME

    # Sanitize extension: only allow alphanumeric characters.
    if not ext.isalnum():
        return _DEFAULT_MIME

    return _MIME_MAP.get(ext, _DEFAULT_MIME)
