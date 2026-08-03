"""MIME Type Guesser module."""

import mimetypes
from pathlib import Path


def guess_mime(filename: str) -> str:
    """
    Guess the MIME type based on file extension.
    
    Args:
        filename: The filename to guess the MIME type for.
        
    Returns:
        The MIME type as a string, or "application/octet-stream" if unknown.
        
    Raises:
        TypeError: If filename is not a string.
    """
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    
    if not filename:
        return "application/octet-stream"
    
    # Get the file extension (case-insensitive)
    path = Path(filename)
    suffix = path.suffix.lower()
    
    if not suffix:
        return "application/octet-stream"
    
    # Use mimetypes to guess the MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    
    if mime_type is None:
        return "application/octet-stream"
    
    return mime_type
