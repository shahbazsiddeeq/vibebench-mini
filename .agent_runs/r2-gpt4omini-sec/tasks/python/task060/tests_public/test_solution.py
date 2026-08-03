import os
import stat
from unittest import mock

import pytest
from src.solution import atomic_write


def test_overwrites(tmp_path):
    p = tmp_path / "out.txt"
    p.write_text("old")
    atomic_write(str(p), "new")
    assert p.read_text() == "new"


def test_content_correct(tmp_path):
    p = tmp_path / "data.txt"
    content = "line1\nline2\nline3"
    atomic_write(str(p), content)
    assert p.read_text() == content


def test_preserves_existing_mode(tmp_path):
    p = tmp_path / "config.txt"
    p.write_text("old")
    os.chmod(str(p), 0o644)
    atomic_write(str(p), "new")
    mode = stat.S_IMODE(os.stat(str(p)).st_mode)
    assert mode == 0o644
    assert p.read_text() == "new"


def test_no_temp_left_on_error(tmp_path):
    p = tmp_path / "out.txt"

    with mock.patch.object(os, "replace", side_effect=OSError("boom")):
        with pytest.raises(OSError):
            atomic_write(str(p), "data")
    # neither the target nor any temp file should remain
    assert list(tmp_path.iterdir()) == []
