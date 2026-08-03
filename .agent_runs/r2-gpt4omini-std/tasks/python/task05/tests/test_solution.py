import os
from pathlib import Path

import pytest
from src.solution import safe_join


def test_inside(tmp_path):
    base = tmp_path / "root"
    (base / "a").mkdir(parents=True)
    p = safe_join(str(base), "a/file.txt")
    assert Path(p).as_posix() == (base.resolve() / "a" / "file.txt").as_posix()


def test_traversal(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "../etc/passwd")


def test_absolute_user_path_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "/etc/passwd")


def test_symlink_escape_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(str(outside), str(base / "link"))
    with pytest.raises(ValueError):
        safe_join(str(base), "link/secret.txt")


def test_nul_byte_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "a\x00b")


def test_harmless_internal_dotdot_allowed(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    p = safe_join(str(base), "a/../b.txt")
    assert Path(p).as_posix() == (base.resolve() / "b.txt").as_posix()
