from __future__ import annotations

import ipaddress


def classify_ip(ip: str) -> dict:
    for version, cls in [(4, ipaddress.IPv4Address), (6, ipaddress.IPv6Address)]:
        try:
            addr = cls(ip)
            return {
                "valid": True,
                "version": version,
                "private": addr.is_private,
                "loopback": addr.is_loopback,
            }
        except ValueError:
            continue
    return {"valid": False, "version": None, "private": False, "loopback": False}
