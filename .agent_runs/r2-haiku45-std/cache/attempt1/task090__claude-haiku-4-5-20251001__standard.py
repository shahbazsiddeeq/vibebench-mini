def guess_mime(filename: str) -> str:
    """
    Guess MIME type based on file extension.
    
    Args:
        filename: The filename to guess MIME type for
        
    Returns:
        The MIME type string, or "application/octet-stream" for unknown types
    """
    # MIME type mapping for common file extensions
    mime_types = {
        'json': 'application/json',
        'pdf': 'application/pdf',
        'html': 'text/html',
        'htm': 'text/html',
        'txt': 'text/plain',
        'css': 'text/css',
        'js': 'application/javascript',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'svg': 'image/svg+xml',
        'ico': 'image/x-icon',
        'xml': 'application/xml',
        'csv': 'text/csv',
        'zip': 'application/zip',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'wav': 'audio/wav',
        'woff': 'font/woff',
        'woff2': 'font/woff2',
        'ttf': 'font/ttf',
        'otf': 'font/otf',
    }
    
    # Extract the file extension (last part after the last dot)
    if '.' not in filename:
        return "application/octet-stream"
    
    # Get the extension and convert to lowercase for case-insensitive matching
    extension = filename.rsplit('.', 1)[-1].lower()
    
    # Return the MIME type or default to application/octet-stream
    return mime_types.get(extension, "application/octet-stream")
