# src/solution.py

def guess_mime(filename: str) -> str:
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
    
    # Split the filename to get the extension
    parts = filename.rsplit('.', 1)
    
    # Check if there is an extension
    if len(parts) > 1:
        extension = parts[-1].lower()
        return mime_types.get(extension, 'application/octet-stream')
    
    return 'application/octet-stream'
