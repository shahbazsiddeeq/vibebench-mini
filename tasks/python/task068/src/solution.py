from __future__ import annotations

import hmac


def secure_compare(a: str, b: str) -> bool:
    # Encode to bytes first: hmac.compare_digest rejects str containing
    # non-ASCII code points, so comparing bytes keeps it robust (and
    # constant-time) for arbitrary Unicode input.
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))
