"""Utilities for determining MIME types from filename extensions."""

from __future__ import annotations

import os
from typing import Final

_DEFAULT_MIME: Final[str] = "application/octet-stream"

_MIME_TYPES: Final[dict[str, str]] = {
    # Text and document formats
    ".txt": "text/plain",
    ".text": "text/plain",
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".csv": "text/csv",
    ".xml": "application/xml",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".rtf": "application/rtf",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    # Scripts and data
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".wasm": "application/wasm",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
    # Images
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".avif": "image/avif",
    # Audio
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".oga": "audio/ogg",
    ".flac": "audio/flac",
    ".aac": "audio/aac",
    ".m4a": "audio/mp4",
    # Video
    ".mp4": "video/mp4",
    ".mpeg": "video/mpeg",
    ".mpg": "video/mpeg",
    ".webm": "video/webm",
    ".ogv": "video/ogg",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    # Archives and binary formats
    ".zip": "application/zip",
    ".gz": "application/gzip",
    ".gzip": "application/gzip",
    ".tar": "application/x-tar",
    ".bz2": "application/x-bzip2",
    ".7z": "application/x-7z-compressed",
    ".rar": "application/vnd.rar",
    ".bin": "application/octet-stream",
    # Fonts
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    # Microsoft Office
    ".doc": "application/msword",
    ".docx": (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    ),
    ".xls": "application/vnd.ms-excel",
    ".xlsx": (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": (
        "application/vnd.openxmlformats-officedocument."
        "presentationml.presentation"
    ),
}


def guess_mime(filename: str) -> str:
    """Return the MIME type associated with a filename's last extension.

    Unknown extensions, filenames without extensions, and invalid inputs use
    the generic binary MIME type.
    """
    if not isinstance(filename, str) or not filename or "\x00" in filename:
        return _DEFAULT_MIME

    extension = os.path.splitext(filename)[1].lower()
    return _MIME_TYPES.get(extension, _DEFAULT_MIME)
