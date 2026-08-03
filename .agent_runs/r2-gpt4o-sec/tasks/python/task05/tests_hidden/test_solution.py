import os
from pathlib import Path

import pytest
from src.solution import safe_join


def test_inside(tmp_path):
    base = tmp_path / "root"
    (base / "a").mkdir(parents=True)
    p = safe_join(str(base), "a/file.txt")
    assert Path(p).as_posix() == (base.resolve() / "a" / "file.txt").as_posix()


def test_absolute_user_path_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "/etc/passwd")


def test_nul_byte_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "a\x00b")
