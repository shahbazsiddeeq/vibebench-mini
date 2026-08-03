from src.solution import sanitize_html














# --- XSS bypass attempts: these must NOT let live markup through ---


def test_keeps_allowed():
    result = sanitize_html("<p>hello</p>", ["p"])
    assert "<p>hello</p>" == result


def test_empty_string():
    assert sanitize_html("", ["b"]) == ""


def test_strips_attributes():
    result = sanitize_html('<a href="x">link</a>', ["a"])
    assert "href" not in result
    assert "link" in result
    assert result == "<a>link</a>"


def test_allowed_tag_strips_event_handler():
    result = sanitize_html("<img src=x onerror=alert(1)>", ["img"])
    assert result == "<img>"
    assert "onerror" not in result
    assert "alert" not in result


def test_attribute_containing_gt_does_not_leak():
    # A naive regex sanitizer stops the tag at the first '>' inside the quoted
    # attribute and leaks the rest as text.
    result = sanitize_html('<a title="foo > bar" href=x>hi</a>', ["a"])
    assert result == "<a>hi</a>"
    assert "bar" not in result


def test_unterminated_script_tag():
    result = sanitize_html("<script>alert(1)", [])
    assert "<script" not in result.lower()
    # script content is dropped (secure), not preserved as text
    assert result == ""
