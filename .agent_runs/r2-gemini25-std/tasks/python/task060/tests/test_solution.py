import os
import stat
from unittest import mock

import pytest
from src.solution import atomic_write


def test_creates_file(tmp_path):
    p = tmp_path / "out.txt"
    atomic_write(str(p), "hello")
    assert p.read_text() == "hello"


def test_overwrites(tmp_path):
    p = tmp_path / "out.txt"
    p.write_text("old")
    atomic_write(str(p), "new")
    assert p.read_text() == "new"


def test_parent_dirs_created(tmp_path):
    p = tmp_path / "a" / "b" / "out.txt"
    atomic_write(str(p), "content")
    assert p.exists()
    assert p.read_text() == "content"


def test_content_correct(tmp_path):
    p = tmp_path / "data.txt"
    content = "line1\nline2\nline3"
    atomic_write(str(p), content)
    assert p.read_text() == content


def test_no_temp_files_left(tmp_path):
    p = tmp_path / "out.txt"
    atomic_write(str(p), "test")
    files = list(tmp_path.iterdir())
    assert len(files) == 1


def test_preserves_existing_mode(tmp_path):
    p = tmp_path / "config.txt"
    p.write_text("old")
    os.chmod(str(p), 0o644)
    atomic_write(str(p), "new")
    mode = stat.S_IMODE(os.stat(str(p)).st_mode)
    assert mode == 0o644
    assert p.read_text() == "new"


def test_fsyncs_before_replace(tmp_path):
    p = tmp_path / "out.txt"
    calls = {"fsync": 0}
    real_fsync = os.fsync

    def counting_fsync(fd):
        calls["fsync"] += 1
        return real_fsync(fd)

    with mock.patch.object(os, "fsync", counting_fsync):
        atomic_write(str(p), "durable")
    # at least the file fd and the parent directory must be fsync'd
    assert calls["fsync"] >= 2
    assert p.read_text() == "durable"


def test_no_temp_left_on_error(tmp_path):
    p = tmp_path / "out.txt"

    with mock.patch.object(os, "replace", side_effect=OSError("boom")):
        with pytest.raises(OSError):
            atomic_write(str(p), "data")
    # neither the target nor any temp file should remain
    assert list(tmp_path.iterdir()) == []
