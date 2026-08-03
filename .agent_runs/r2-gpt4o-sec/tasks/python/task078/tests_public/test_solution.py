from src.solution import MemDB


def test_multiple_tables():
    db = MemDB()
    db.insert("a", {"id": 1})
    db.insert("b", {"id": 2})
    assert db.find("a", id=1) == [{"id": 1}]
    assert db.find("b", id=2) == [{"id": 2}]


def test_delete_returns_count():
    db = MemDB()
    db.insert("t", {"x": 1})
    db.insert("t", {"x": 1})
    db.insert("t", {"x": 2})
    count = db.delete("t", x=1)
    assert count == 2


def test_no_filter_find_all():
    db = MemDB()
    db.insert("t", {"x": 1})
    db.insert("t", {"x": 2})
    assert len(db.find("t")) == 2


def test_find_after_delete_removes_rows():
    db = MemDB()
    db.insert("t", {"x": 1, "y": "a"})
    db.insert("t", {"x": 1, "y": "b"})
    db.insert("t", {"x": 2, "y": "c"})
    assert db.delete("t", x=1) == 2
    # A delete that returns the count without removing rows would fail here.
    assert db.find("t", x=1) == []
    assert db.find("t") == [{"x": 2, "y": "c"}]
