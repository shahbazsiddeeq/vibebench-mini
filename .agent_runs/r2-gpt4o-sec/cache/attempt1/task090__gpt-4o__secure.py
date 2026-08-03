# src/solution.py

def guess_mime(filename):
    import os

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
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
        'flv': 'video/x-flv',
        'mkv': 'video/x-matroska',
        'bmp': 'image/bmp',
        'webp': 'image/webp',
        'ico': 'image/vnd.microsoft.icon',
        'svg': 'image/svg+xml',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'midi': 'audio/midi',
        'mid': 'audio/midi',
        'rtf': 'application/rtf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }

    # Extract the file extension
    _, ext = os.path.splitext(filename)
    ext = ext.lower().lstrip('.')

    # Return the corresponding MIME type or default to 'application/octet-stream'
    return mime_types.get(ext, 'application/octet-stream')
