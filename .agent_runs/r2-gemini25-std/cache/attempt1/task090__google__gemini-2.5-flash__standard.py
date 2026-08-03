import os

def guess_mime(filename: str) -> str:
    """
    Guesses the MIME type based on the file extension.

    Args:
        filename: The name of the file, including its extension.

    Returns:
        The guessed MIME type as a string. Defaults to "application/octet-stream"
        if the extension is unknown or missing.
    """
    _MIME_TYPES = {
        # Text types
        "txt": "text/plain",
        "html": "text/html",
        "htm": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "xml": "application/xml",
        "csv": "text/csv",
        "tsv": "text/tab-separated-values",
        "md": "text/markdown",
        "yaml": "text/yaml",
        "yml": "text/yaml",

        # Image types
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "svg": "image/svg+xml",
        "webp": "image/webp",
        "ico": "image/x-icon",

        # Audio types
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "aac": "audio/aac",
        "flac": "audio/flac",

        # Video types
        "mp4": "video/mp4",
        "mpeg": "video/mpeg",
        "avi": "video/x-msvideo",
        "mov": "video/quicktime",
        "wmv": "video/x-ms-wmv",
        "flv": "video/x-flv",
        "webm": "video/webm",

        # Application types
        "pdf": "application/pdf",
        "zip": "application/zip",
        "tar": "application/x-tar",
        "gz": "application/gzip",
        "rar": "application/x-rar-compressed",
        "7z": "application/x-7z-compressed",
        "exe": "application/x-msdownload",
        "dll": "application/x-msdownload",
        "bin": "application/octet-stream",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "odt": "application/vnd.oasis.opendocument.text",
        "ods": "application/vnd.oasis.opendocument.spreadsheet",
        "odp": "application/vnd.oasis.opendocument.presentation",
        "rtf": "application/rtf",
        "sh": "application/x-sh",
        "py": "text/x-python",
        "java": "text/x-java-source",
        "c": "text/x-c",
        "cpp": "text/x-c++src",
        "h": "text/x-chdr",
        "hpp": "text/x-c++hdr",
        "php": "application/x-httpd-php",
        "rb": "application/x-ruby",
        "pl": "application/x-perl",
        "pm": "application/x-perl",
        "sql": "application/sql",
        "wasm": "application/wasm",
    }

    _, ext = os.path.splitext(filename)
    if ext:
        # Remove the leading dot and convert to lowercase for case-insensitivity
        ext = ext[1:].lower()
        return _MIME_TYPES.get(ext, "application/octet-stream")
    else:
        return "application/octet-stream"
