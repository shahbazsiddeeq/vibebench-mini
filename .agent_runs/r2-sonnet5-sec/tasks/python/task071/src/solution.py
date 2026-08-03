"""
IP Address Classifier

Provides classify_ip(ip) which validates a string as an IPv4 or IPv6
address (strict, no CIDR notation, no port suffix) and reports whether
it falls into a private / reserved range or is a loopback address, per
Python's ipaddress module semantics (which mirror the IANA special-
purpose address registries).
"""

import ipaddress
from typing import Any, Dict


def classify_ip(ip: Any) -> Dict[str, Any]:
    """
    Classify a string as an IPv4/IPv6 address.

    Returns a dict:
        {
            "valid": bool,
            "version": 4 | 6 | None,
            "private": bool,
            "loopback": bool,
        }

    Any invalid, malformed, or unexpected input results in:
        {"valid": False, "version": None, "private": False, "loopback": False}

    Only plain addresses are accepted -- no CIDR notation (e.g. "/24")
    and no port suffixes (e.g. ":8080").
    """
    default_result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False,
    }

    # Strict input validation: must be a non-empty string.
    if not isinstance(ip, str):
        return default_result

    candidate = ip.strip()
    if not candidate:
        return default_result

    # Reject CIDR notation explicitly.
    if "/" in candidate:
        return default_result

    try:
        addr = ipaddress.ip_address(candidate)
    except (ValueError, TypeError):
        return default_result

    try:
        is_private = bool(addr.is_private)
        is_loopback = bool(addr.is_loopback)
        version = addr.version
    except Exception:
        # Defensive: never leak internals, just report invalid.
        return default_result

    return {
        "valid": True,
        "version": version,
        "private": is_private,
        "loopback": is_loopback,
    }
