"""
URL Parser module - securely parses URLs into components.
"""

from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional, Union


def parse_url(url: str) -> Dict[str, Any]:
    """
    Parse a URL into its components.
    
    Args:
        url: A URL string to parse
        
    Returns:
        A dictionary with keys: scheme, host, port, path, query_params, fragment
        
    Raises:
        ValueError: If scheme or host is missing
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")
    
    if not url.strip():
        raise ValueError("URL cannot be empty")
    
    # Use urllib.parse for safe URL parsing
    parsed = urlparse(url)
    
    # Validate required components
    scheme = parsed.scheme
    if not scheme:
        raise ValueError("Scheme is missing")
    
    host = parsed.hostname
    if not host:
        raise ValueError("Host is missing")
    
    # Lowercase the host
    host = host.lower()
    
    # Extract port (int or None)
    port: Optional[int] = parsed.port
    
    # Extract path (default to "/" if empty)
    path = parsed.path if parsed.path else "/"
    
    # Parse query parameters
    query_params: Dict[str, Union[str, list]] = {}
    if parsed.query:
        # parse_qs returns lists for all values
        raw_params = parse_qs(parsed.query, keep_blank_values=True)
        
        for key, values in raw_params.items():
            # Filter out empty values
            filtered_values = [v for v in values if v]
            
            if filtered_values:
                # If only one value, store as string; otherwise as list
                if len(filtered_values) == 1:
                    query_params[key] = filtered_values[0]
                else:
                    query_params[key] = filtered_values
    
    # Extract fragment (empty string if absent)
    fragment = parsed.fragment if parsed.fragment else ""
    
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
