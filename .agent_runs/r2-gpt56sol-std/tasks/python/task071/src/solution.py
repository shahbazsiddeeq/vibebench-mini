"""Utilities for classifying IPv4 and IPv6 addresses."""

import ipaddress
from typing import Any, Dict, Optional, Union


def classify_ip(ip: str) -> Dict[str, Union[bool, Optional[int]]]:
    """Classify an IPv4 or IPv6 address string."""
    invalid: Dict[str, Union[bool, Optional[int]]] = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False,
    }

    if not isinstance(ip, str) or "%" in ip:
        return invalid

    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return invalid

    return {
        "valid": True,
        "version": address.version,
        "private": bool(address.is_private),
        "loopback": bool(address.is_loopback),
    }
