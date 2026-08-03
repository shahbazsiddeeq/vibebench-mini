def guess_mime(filename):
    """
    Guess the MIME type based on file extension.
    
    Args:
        filename: The filename to check
        
    Returns:
        The MIME type string, or "application/octet-stream" for unknown types
    """
    # Common MIME type mappings
    mime_types = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.pdf': 'application/pdf',
        '.zip': 'application/zip',
        '.tar': 'application/x-tar',
        '.gz': 'application/gzip',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.webp': 'image/webp',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.mpeg': 'video/mpeg',
        '.webm': 'video/webm',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }
    
    # Find the last dot in the filename
    last_dot_index = filename.rfind('.')
    
    # If no extension found, return default
    if last_dot_index == -1:
        return 'application/octet-stream'
    
    # Extract extension (including the dot) and convert to lowercase
    extension = filename[last_dot_index:].lower()
    
    # Return the MIME type or default
    return mime_types.get(extension, 'application/octet-stream')
