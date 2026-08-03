import pytest
from src.solution import KVStore


def test_missing_returns_default(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    assert kv.get("missing") is None
    assert kv.get("missing", 99) == 99


def test_delete_missing(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    assert kv.delete("nonexistent") is False


def test_invalid_key_raises(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    with pytest.raises(ValueError):
        kv.set("bad/key", "val")


def test_delete_persists_across_reopen(tmp_path):
    path = str(tmp_path / "store.json")
    kv1 = KVStore(path)
    kv1.set("a", 1)
    kv1.set("b", 2)
    assert kv1.delete("a") is True
    # A store that never writes the deletion to disk would still see "a" here.
    kv2 = KVStore(path)
    assert kv2.get("a") is None
    assert kv2.get("b") == 2
    assert set(kv2.keys()) == {"b"}
