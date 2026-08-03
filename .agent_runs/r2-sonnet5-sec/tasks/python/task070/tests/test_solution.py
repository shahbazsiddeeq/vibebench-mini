from src.solution import sanitize_html


def test_removes_script():
    result = sanitize_html("<b>Hi</b> <script>bad</script>", ["b"])
    assert "<script>" not in result
    assert "bad" in result
    assert "<b>Hi</b>" in result


def test_keeps_allowed():
    result = sanitize_html("<p>hello</p>", ["p"])
    assert "<p>hello</p>" == result


def test_empty_allowed_removes_all():
    result = sanitize_html("<b>text</b>", [])
    assert result == "text"


def test_empty_string():
    assert sanitize_html("", ["b"]) == ""


def test_case_insensitive_allowed():
    result = sanitize_html("<B>bold</B>", ["b"])
    assert "bold" in result


def test_strips_attributes():
    result = sanitize_html('<a href="x">link</a>', ["a"])
    assert "href" not in result
    assert "link" in result
    assert result == "<a>link</a>"


# --- XSS bypass attempts: these must NOT let live markup through ---


def test_disallowed_tag_with_event_handler_removed():
    result = sanitize_html("<img src=x onerror=alert(1)>", ["b"])
    assert result == ""
    assert "onerror" not in result
    assert "img" not in result


def test_allowed_tag_strips_event_handler():
    result = sanitize_html("<img src=x onerror=alert(1)>", ["img"])
    assert result == "<img>"
    assert "onerror" not in result
    assert "alert" not in result


def test_javascript_url_attribute_stripped():
    result = sanitize_html('<a href="javascript:alert(1)">x</a>', ["a"])
    assert result == "<a>x</a>"
    assert "javascript" not in result


def test_attribute_containing_gt_does_not_leak():
    # A naive regex sanitizer stops the tag at the first '>' inside the quoted
    # attribute and leaks the rest as text.
    result = sanitize_html('<a title="foo > bar" href=x>hi</a>', ["a"])
    assert result == "<a>hi</a>"
    assert "bar" not in result


def test_nested_reemerging_script_tag():
    # Removing "<script>" once would re-form a live "<script>" here.
    result = sanitize_html("<scr<script>ipt>alert(1)</script>", [])
    assert "<script" not in result.lower()
    assert ">" not in result  # any leftover angle brackets are escaped


def test_unterminated_script_tag():
    result = sanitize_html("<script>alert(1)", [])
    assert "<script" not in result.lower()
    # script content is dropped (secure), not preserved as text
    assert result == ""


def test_stray_angle_brackets_escaped():
    # Plain text with angle brackets must be escaped, not passed through.
    assert sanitize_html("a < b and c > d", []) == "a &lt; b and c &gt; d"
