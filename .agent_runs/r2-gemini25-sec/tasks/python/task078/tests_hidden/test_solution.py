from src.solution import MemDB


def test_insert_find():
    db = MemDB()
    db.insert("t", {"x": 1, "y": "a"})
    result = db.find("t", x=1)
    assert result == [{"x": 1, "y": "a"}]


def test_filter_no_match():
    db = MemDB()
    db.insert("t", {"x": 1})
    assert db.find("t", x=2) == []


def test_find_empty_table():
    db = MemDB()
    assert db.find("missing") == []


def test_find_multiple_filters_are_anded():
    db = MemDB()
    db.insert("t", {"x": 1, "y": "a"})
    db.insert("t", {"x": 1, "y": "b"})
    db.insert("t", {"x": 2, "y": "a"})
    # Both filters must match; a solution applying only the first filter fails.
    assert db.find("t", x=1, y="a") == [{"x": 1, "y": "a"}]
    assert db.find("t", x=1, y="b") == [{"x": 1, "y": "b"}]
    assert db.find("t", x=2, y="b") == []
