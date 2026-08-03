import pytest
from src.solution import KVStore


def test_set_get(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("x", 42)
    assert kv.get("x") == 42


def test_missing_returns_default(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    assert kv.get("missing") is None
    assert kv.get("missing", 99) == 99


def test_delete_existing(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("k", "v")
    assert kv.delete("k") is True
    assert kv.get("k") is None


def test_delete_missing(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    assert kv.delete("nonexistent") is False


def test_keys(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("a", 1)
    kv.set("b", 2)
    assert set(kv.keys()) == {"a", "b"}


def test_invalid_key_raises(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    with pytest.raises(ValueError):
        kv.set("bad/key", "val")


def test_persistence(tmp_path):
    path = str(tmp_path / "store.json")
    kv1 = KVStore(path)
    kv1.set("p", "persistent")
    kv2 = KVStore(path)
    assert kv2.get("p") == "persistent"


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


def test_non_scalar_values_persist(tmp_path):
    path = str(tmp_path / "store.json")
    kv1 = KVStore(path)
    kv1.set("list", [1, 2, 3])
    kv1.set("dict", {"nested": {"k": "v"}})
    kv2 = KVStore(path)
    assert kv2.get("list") == [1, 2, 3]
    assert kv2.get("dict") == {"nested": {"k": "v"}}
