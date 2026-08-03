import re
from datetime import datetime

from src.solution import append_log


def test_appends_multiple(tmp_path):
    p = tmp_path / "test.log"
    append_log(str(p), "msg1", timestamp=False)
    append_log(str(p), "msg2", timestamp=False)
    lines = p.read_text().splitlines()
    assert lines == ["msg1", "msg2"]


def test_no_timestamp(tmp_path):
    p = tmp_path / "test.log"
    append_log(str(p), "plain", timestamp=False)
    assert p.read_text().strip() == "plain"
