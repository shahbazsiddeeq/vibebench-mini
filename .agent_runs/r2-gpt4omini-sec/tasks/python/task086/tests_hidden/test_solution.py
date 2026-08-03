from src.solution import parse_robots

ROBOTS = """
User-agent: *
Disallow: /private
Allow: /public
Crawl-delay: 2

User-agent: Googlebot
Disallow: /google-only
"""


def test_wildcard_disallow():
    result = parse_robots(ROBOTS, "*")
    assert "/private" in result["disallowed"]


def test_crawl_delay():
    result = parse_robots(ROBOTS, "*")
    assert result["crawl_delay"] == 2.0


def test_fallback_to_wildcard():
    result = parse_robots(ROBOTS, "UnknownBot")
    assert "/private" in result["disallowed"]


def test_comment_in_group_does_not_reset():
    content = (
        "User-agent: *\n"
        "Disallow: /private\n"
        "# a mid-group comment must not wipe the group\n"
        "Disallow: /secret\n"
    )
    result = parse_robots(content, "*")
    assert result["disallowed"] == ["/private", "/secret"]


def test_user_agent_directive_case_insensitive():
    content = "User-Agent: BadBot\nDisallow: /x\n"
    result = parse_robots(content, "badbot")
    assert result["disallowed"] == ["/x"]
