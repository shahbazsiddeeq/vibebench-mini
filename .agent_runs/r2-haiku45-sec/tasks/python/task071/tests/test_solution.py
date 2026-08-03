from src.solution import classify_ip


def test_valid_public_ipv4():
    r = classify_ip("8.8.8.8")
    assert r["valid"] is True
    assert r["version"] == 4
    assert r["private"] is False
    assert r["loopback"] is False


def test_private_ipv4():
    r = classify_ip("192.168.1.1")
    assert r["valid"] is True
    assert r["private"] is True


def test_loopback_ipv4():
    r = classify_ip("127.0.0.1")
    assert r["loopback"] is True


def test_invalid():
    r = classify_ip("999.999.999.999")
    assert r["valid"] is False
    assert r["version"] is None


def test_valid_ipv6():
    r = classify_ip("::1")
    assert r["valid"] is True
    assert r["version"] == 6
    assert r["loopback"] is True


def test_private_10x():
    r = classify_ip("10.0.0.1")
    assert r["private"] is True


def test_172_boundaries():
    # 172.16.0.0 - 172.31.255.255 is private; just outside is not
    assert classify_ip("172.15.255.255")["private"] is False
    assert classify_ip("172.16.0.0")["private"] is True
    assert classify_ip("172.31.255.255")["private"] is True
    assert classify_ip("172.32.0.0")["private"] is False


def test_cgnat_not_private():
    # 100.64.0.0/10 (carrier-grade NAT) is NOT counted as private here
    assert classify_ip("100.64.0.1")["private"] is False


def test_special_ranges_private():
    assert classify_ip("0.0.0.0")["private"] is True
    assert classify_ip("192.0.2.1")["private"] is True  # TEST-NET-1


def test_public_ipv6():
    r = classify_ip("2606:4700:4700::1111")
    assert r["valid"] is True
    assert r["version"] == 6
    assert r["private"] is False
    assert r["loopback"] is False


def test_ipv6_link_local_and_doc_private():
    assert classify_ip("fe80::1")["private"] is True
    assert classify_ip("2001:db8::1")["private"] is True
