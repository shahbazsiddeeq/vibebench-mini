def guess_mime(filename):
    """
    Guess the MIME type based on file extension.
    
    Args:
        filename: A string representing the filename
        
    Returns:
        A string representing the MIME type, or "application/octet-stream" for unknown types
    """
    # Validate input
    if not isinstance(filename, str):
        return "application/octet-stream"
    
    # Sanitize filename to prevent path traversal or other issues
    # We only care about the extension, so we can work with the basename
    filename = filename.strip()
    
    if not filename:
        return "application/octet-stream"
    
    # Extract extension (case-insensitive)
    # Find the last dot in the filename
    last_dot_index = filename.rfind('.')
    
    if last_dot_index == -1 or last_dot_index == len(filename) - 1:
        # No extension or dot is at the end
        return "application/octet-stream"
    
    extension = filename[last_dot_index + 1:].lower()
    
    # Common MIME type mappings
    mime_types = {
        # Text
        'html': 'text/html',
        'htm': 'text/html',
        'css': 'text/css',
        'js': 'text/javascript',
        'txt': 'text/plain',
        'csv': 'text/csv',
        'xml': 'text/xml',
        
        # Images
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'svg': 'image/svg+xml',
        'ico': 'image/x-icon',
        'webp': 'image/webp',
        
        # Application
        'json': 'application/json',
        'pdf': 'application/pdf',
        'zip': 'application/zip',
        'gz': 'application/gzip',
        'tar': 'application/x-tar',
        'xml': 'application/xml',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        
        # Audio
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        
        # Video
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mpeg': 'video/mpeg',
        'webm': 'video/webm',
    }
    
    return mime_types.get(extension, "application/octet-stream")
