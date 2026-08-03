import os
from pathlib import Path

import pytest
from src.solution import safe_join


def test_traversal(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(str(base), "../etc/passwd")


def test_symlink_escape_rejected(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(str(outside), str(base / "link"))
    with pytest.raises(ValueError):
        safe_join(str(base), "link/secret.txt")


def test_harmless_internal_dotdot_allowed(tmp_path):
    base = tmp_path / "root"
    base.mkdir()
    p = safe_join(str(base), "a/../b.txt")
    assert Path(p).as_posix() == (base.resolve() / "b.txt").as_posix()
