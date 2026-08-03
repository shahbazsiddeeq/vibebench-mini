from src.solution import parse_robots

ROBOTS = """
User-agent: *
Disallow: /private
Allow: /public
Crawl-delay: 2

User-agent: Googlebot
Disallow: /google-only
"""


def test_wildcard_allow():
    result = parse_robots(ROBOTS, "*")
    assert "/public" in result["allowed"]


def test_specific_agent():
    result = parse_robots(ROBOTS, "Googlebot")
    assert "/google-only" in result["disallowed"]


def test_empty_content():
    result = parse_robots("", "*")
    assert result == {"allowed": [], "disallowed": [], "crawl_delay": None}


def test_user_agent_case_insensitive():
    result = parse_robots(ROBOTS, "googlebot")
    assert "/google-only" in result["disallowed"]
