"""Utilities for determining MIME types from filenames."""

from __future__ import annotations

import os


_DEFAULT_MIME = "application/octet-stream"

_MIME_TYPES = {
    ".7z": "application/x-7z-compressed",
    ".aac": "audio/aac",
    ".avi": "video/x-msvideo",
    ".avif": "image/avif",
    ".bin": "application/octet-stream",
    ".bmp": "image/bmp",
    ".bz": "application/x-bzip",
    ".bz2": "application/x-bzip2",
    ".css": "text/css",
    ".csv": "text/csv",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".epub": "application/epub+zip",
    ".gif": "image/gif",
    ".gz": "application/gzip",
    ".htm": "text/html",
    ".html": "text/html",
    ".ico": "image/x-icon",
    ".jar": "application/java-archive",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "application/javascript",
    ".json": "application/json",
    ".jsonld": "application/ld+json",
    ".md": "text/markdown",
    ".midi": "audio/midi",
    ".mjs": "application/javascript",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".mpeg": "video/mpeg",
    ".odp": "application/vnd.oasis.opendocument.presentation",
    ".ods": "application/vnd.oasis.opendocument.spreadsheet",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".oga": "audio/ogg",
    ".ogg": "audio/ogg",
    ".ogv": "video/ogg",
    ".opus": "audio/opus",
    ".otf": "font/otf",
    ".pdf": "application/pdf",
    ".php": "application/x-httpd-php",
    ".png": "image/png",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".rar": "application/vnd.rar",
    ".rtf": "application/rtf",
    ".svg": "image/svg+xml",
    ".tar": "application/x-tar",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".ts": "video/mp2t",
    ".ttf": "font/ttf",
    ".txt": "text/plain",
    ".wav": "audio/wav",
    ".weba": "audio/webm",
    ".webm": "video/webm",
    ".webp": "image/webp",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".xhtml": "application/xhtml+xml",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xml": "application/xml",
    ".zip": "application/zip",
}


def guess_mime(filename: str) -> str:
    """Return the MIME type inferred from the filename's final extension."""
    if not isinstance(filename, str):
        return _DEFAULT_MIME

    extension = os.path.splitext(filename)[1].lower()
    return _MIME_TYPES.get(extension, _DEFAULT_MIME)
