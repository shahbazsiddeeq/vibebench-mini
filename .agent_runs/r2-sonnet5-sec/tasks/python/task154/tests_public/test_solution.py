import os

import pytest

from src.solution import join_files, split_file


def test_split_exact_multiple(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"ABCD")
    parts = split_file(str(src), 2, str(tmp_path / "o"))
    assert len(parts) == 2
    assert os.path.basename(parts[-1]) == "d.bin.part001"


def test_split_creates_dest_dir(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"xyz")
    dest = tmp_path / "nested" / "made"
    parts = split_file(str(src), 10, str(dest))
    assert parts == [str(dest / "d.bin.part000")]
    assert (dest / "d.bin.part000").read_bytes() == b"xyz"


def test_join_basic(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.write_bytes(b"AB")
    b.write_bytes(b"CDE")
    dest = tmp_path / "joined.bin"
    n = join_files([str(a), str(b)], str(dest))
    assert n == 5
    assert dest.read_bytes() == b"ABCDE"


def test_round_trip(tmp_path):
    payload = bytes(range(256)) * 300  # 76800 bytes
    src = tmp_path / "orig.bin"
    src.write_bytes(payload)
    parts = split_file(str(src), 1000, str(tmp_path / "chunks"))
    restored = tmp_path / "restored.bin"
    n = join_files(parts, str(restored))
    assert n == len(payload)
    assert restored.read_bytes() == payload


def test_split_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError):
        split_file(str(tmp_path / "nope.bin"), 4, str(tmp_path / "o"))
