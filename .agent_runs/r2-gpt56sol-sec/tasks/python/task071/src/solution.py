"""Utilities for classifying IPv4 and IPv6 addresses."""

import ipaddress
from typing import Any, Dict, Optional, Union


def classify_ip(ip: Any) -> Dict[str, Union[bool, Optional[int]]]:
    """Classify a textual IPv4 or IPv6 address."""
    invalid: Dict[str, Union[bool, Optional[int]]] = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False,
    }

    if not isinstance(ip, str) or not ip or len(ip) > 45:
        return invalid

    # Scoped addresses are interface-qualified addresses, not plain IP addresses.
    if "%" in ip:
        return invalid

    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return invalid

    return {
        "valid": True,
        "version": address.version,
        "private": address.is_private,
        "loopback": address.is_loopback,
    }
