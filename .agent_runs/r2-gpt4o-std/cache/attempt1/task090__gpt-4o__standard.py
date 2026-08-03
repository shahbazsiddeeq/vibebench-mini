# src/solution.py

def guess_mime(filename):
    # Mapping of file extensions to MIME types
    mime_types = {
        'html': 'text/html',
        'htm': 'text/html',
        'txt': 'text/plain',
        'css': 'text/css',
        'csv': 'text/csv',
        'json': 'application/json',
        'xml': 'application/xml',
        'js': 'application/javascript',
        'pdf': 'application/pdf',
        'zip': 'application/zip',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'webp': 'image/webp',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
    }
    
    # Extract the file extension
    parts = filename.lower().rsplit('.', 1)
    if len(parts) == 2:
        extension = parts[1]
        return mime_types.get(extension, 'application/octet-stream')
    else:
        return 'application/octet-stream'
