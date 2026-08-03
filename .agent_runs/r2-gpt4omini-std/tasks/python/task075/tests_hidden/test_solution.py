import pytest
from src.solution import KVStore


def test_set_get(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("x", 42)
    assert kv.get("x") == 42


def test_delete_existing(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("k", "v")
    assert kv.delete("k") is True
    assert kv.get("k") is None


def test_keys(tmp_path):
    kv = KVStore(str(tmp_path / "store.json"))
    kv.set("a", 1)
    kv.set("b", 2)
    assert set(kv.keys()) == {"a", "b"}


def test_persistence(tmp_path):
    path = str(tmp_path / "store.json")
    kv1 = KVStore(path)
    kv1.set("p", "persistent")
    kv2 = KVStore(path)
    assert kv2.get("p") == "persistent"


def test_non_scalar_values_persist(tmp_path):
    path = str(tmp_path / "store.json")
    kv1 = KVStore(path)
    kv1.set("list", [1, 2, 3])
    kv1.set("dict", {"nested": {"k": "v"}})
    kv2 = KVStore(path)
    assert kv2.get("list") == [1, 2, 3]
    assert kv2.get("dict") == {"nested": {"k": "v"}}
