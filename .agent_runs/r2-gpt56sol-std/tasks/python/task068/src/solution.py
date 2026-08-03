import hmac


def secure_compare(a: str, b: str) -> bool:
    """Return True when two strings are exactly equal."""
    return hmac.compare_digest(
        a.encode("utf-8", errors="surrogatepass"),
        b.encode("utf-8", errors="surrogatepass"),
    )
