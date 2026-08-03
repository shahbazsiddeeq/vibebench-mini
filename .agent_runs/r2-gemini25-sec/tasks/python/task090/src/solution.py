import os

def guess_mime(filename: str) -> str:
    """
    Guesses the MIME type of a file based on its extension.

    Args:
        filename: The name of the file, including its extension.

    Returns:
        The guessed MIME type as a string. Returns "application/octet-stream"
        if the extension is unknown or missing.
    """
    if not isinstance(filename, str):
        # While the type hint suggests str, robust code handles unexpected types.
        # For this specific problem, an empty string or non-string input
        # should probably lead to the default MIME type.
        return "application/octet-stream"

    # Sanitize filename to prevent path traversal or other issues if it were
    # ever used in a context that interacts with the filesystem.
    # For this specific function, it's primarily about extracting the extension,
    # but it's good practice to consider potential misuse.
    filename = os.path.basename(filename)

    # Define a dictionary of common MIME types.
    # This approach is secure as it's a static lookup table.
    # No external data is used directly to construct MIME types.
    MIME_TYPES = {
        ".html": "text/html",
        ".htm": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".xml": "application/xml",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".pdf": "application/pdf",
        ".zip": "application/zip",
        ".tar": "application/x-tar",
        ".gz": "application/gzip",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".ogg": "application/ogg", # Can be audio or video
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".py": "text/x-python",
        ".java": "text/x-java-source",
        ".c": "text/x-c",
        ".cpp": "text/x-c++src",
        ".h": "text/x-chdr",
        ".sh": "application/x-sh",
        ".md": "text/markdown",
        ".yaml": "application/x-yaml",
        ".yml": "application/x-yaml",
    }

    # Extract the file extension.
    # os.path.splitext handles cases with no extension or multiple dots correctly.
    # It returns a tuple (root, ext). We are interested in ext.
    _, ext = os.path.splitext(filename)

    # Convert extension to lowercase for case-insensitive matching.
    ext_lower = ext.lower()

    # Look up the MIME type in the dictionary.
    # Use .get() with a default value to avoid KeyError for unknown extensions.
    return MIME_TYPES.get(ext_lower, "application/octet-stream")
