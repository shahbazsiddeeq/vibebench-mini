from src.solution import classify_ip


def test_private_ipv4():
    r = classify_ip("192.168.1.1")
    assert r["valid"] is True
    assert r["private"] is True


def test_invalid():
    r = classify_ip("999.999.999.999")
    assert r["valid"] is False
    assert r["version"] is None


def test_private_10x():
    r = classify_ip("10.0.0.1")
    assert r["private"] is True


def test_cgnat_not_private():
    # 100.64.0.0/10 (carrier-grade NAT) is NOT counted as private here
    assert classify_ip("100.64.0.1")["private"] is False


def test_public_ipv6():
    r = classify_ip("2606:4700:4700::1111")
    assert r["valid"] is True
    assert r["version"] == 6
    assert r["private"] is False
    assert r["loopback"] is False
