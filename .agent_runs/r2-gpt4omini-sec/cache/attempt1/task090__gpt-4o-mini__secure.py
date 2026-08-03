# src/solution.py

import os

def guess_mime(filename: str) -> str:
    # Define a mapping of file extensions to MIME types
    mime_types = {
        'html': 'text/html',
        'htm': 'text/html',
        'json': 'application/json',
        'pdf': 'application/pdf',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'txt': 'text/plain',
        'csv': 'text/csv',
        'xml': 'application/xml',
        'zip': 'application/zip',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',
        'mp4': 'video/mp4',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ico': 'image/x-icon',
    }

    # Validate input
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")

    # Extract the file extension
    _, ext = os.path.splitext(filename)
    
    # Normalize the extension to lower case and remove the leading dot
    ext = ext[1:].lower() if ext else ''

    # Return the corresponding MIME type or the default
    return mime_types.get(ext, 'application/octet-stream')
