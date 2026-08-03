import os

import pytest

from src.solution import join_files, split_file


def test_split_basic(tmp_path):
    src = tmp_path / "data.bin"
    src.write_bytes(b"ABCDE")
    dest = tmp_path / "out"
    parts = split_file(str(src), 2, str(dest))
    assert parts == [
        str(dest / "data.bin.part000"),
        str(dest / "data.bin.part001"),
        str(dest / "data.bin.part002"),
    ]
    assert (dest / "data.bin.part000").read_bytes() == b"AB"
    assert (dest / "data.bin.part001").read_bytes() == b"CD"
    assert (dest / "data.bin.part002").read_bytes() == b"E"


def test_split_exact_multiple(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"ABCD")
    parts = split_file(str(src), 2, str(tmp_path / "o"))
    assert len(parts) == 2
    assert os.path.basename(parts[-1]) == "d.bin.part001"


def test_split_empty_file_returns_empty(tmp_path):
    src = tmp_path / "empty.bin"
    src.write_bytes(b"")
    dest = tmp_path / "o"
    parts = split_file(str(src), 4, str(dest))
    assert parts == []
    assert os.path.isdir(str(dest))
    assert os.listdir(str(dest)) == []


def test_split_creates_dest_dir(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"xyz")
    dest = tmp_path / "nested" / "made"
    parts = split_file(str(src), 10, str(dest))
    assert parts == [str(dest / "d.bin.part000")]
    assert (dest / "d.bin.part000").read_bytes() == b"xyz"


def test_split_chunk_larger_than_file(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"hello")
    parts = split_file(str(src), 100, str(tmp_path / "o"))
    assert len(parts) == 1
    assert open(parts[0], "rb").read() == b"hello"


def test_join_basic(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.write_bytes(b"AB")
    b.write_bytes(b"CDE")
    dest = tmp_path / "joined.bin"
    n = join_files([str(a), str(b)], str(dest))
    assert n == 5
    assert dest.read_bytes() == b"ABCDE"


def test_join_empty_list(tmp_path):
    dest = tmp_path / "joined.bin"
    n = join_files([], str(dest))
    assert n == 0
    assert dest.read_bytes() == b""


def test_round_trip(tmp_path):
    payload = bytes(range(256)) * 300  # 76800 bytes
    src = tmp_path / "orig.bin"
    src.write_bytes(payload)
    parts = split_file(str(src), 1000, str(tmp_path / "chunks"))
    restored = tmp_path / "restored.bin"
    n = join_files(parts, str(restored))
    assert n == len(payload)
    assert restored.read_bytes() == payload


def test_split_invalid_chunk_size(tmp_path):
    src = tmp_path / "d.bin"
    src.write_bytes(b"x")
    with pytest.raises(ValueError):
        split_file(str(src), 0, str(tmp_path / "o"))


def test_split_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError):
        split_file(str(tmp_path / "nope.bin"), 4, str(tmp_path / "o"))


def test_join_missing_part(tmp_path):
    with pytest.raises(FileNotFoundError):
        join_files([str(tmp_path / "nope")], str(tmp_path / "out.bin"))
