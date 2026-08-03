import re
from datetime import datetime

from src.solution import append_log


def test_creates_file(tmp_path):
    p = tmp_path / "test.log"
    append_log(str(p), "hello")
    assert p.exists()


def test_timestamp_prefix(tmp_path):
    p = tmp_path / "test.log"
    append_log(str(p), "event")
    content = p.read_text()
    assert content.endswith("\n")
    line = content.rstrip("\n")
    m = re.fullmatch(
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00) event", line
    )
    assert m is not None, line
    # the prefix must be a valid ISO-8601 timestamp
    datetime.fromisoformat(m.group(1))


def test_parent_dirs_created(tmp_path):
    p = tmp_path / "a" / "b" / "test.log"
    append_log(str(p), "msg", timestamp=False)
    assert p.exists()
