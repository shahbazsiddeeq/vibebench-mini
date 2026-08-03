"""
MIME Type Guesser

Provides guess_mime(filename) which returns the MIME type based on the
file's extension (case-insensitive), falling back to
"application/octet-stream" for unknown or missing extensions.
"""

_MIME_TYPES = {
    "html": "text/html",
    "htm": "text/html",
    "txt": "text/plain",
    "css": "text/css",
    "csv": "text/csv",
    "json": "application/json",
    "xml": "application/xml",
    "js": "application/javascript",
    "pdf": "application/pdf",
    "zip": "application/zip",
    "gz": "application/gzip",
    "tar": "application/x-tar",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "svg": "image/svg+xml",
    "ico": "image/vnd.microsoft.icon",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "mp4": "video/mp4",
    "avi": "video/x-msvideo",
    "mov": "video/quicktime",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def guess_mime(filename):
    """
    Return the MIME type for a given filename based on its extension.

    The lookup is case-insensitive and uses the last extension when
    multiple dots are present. Returns "application/octet-stream" if
    no extension is found or the extension is unrecognized.
    """
    if not filename:
        return "application/octet-stream"

    # Extract the last segment after the final dot, if any.
    base = filename.rsplit("/", 1)[-1]
    if "." not in base:
        return "application/octet-stream"

    ext = base.rsplit(".", 1)[-1].lower()
    return _MIME_TYPES.get(ext, "application/octet-stream")
