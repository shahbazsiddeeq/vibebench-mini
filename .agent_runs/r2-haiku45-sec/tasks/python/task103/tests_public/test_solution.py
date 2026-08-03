from src.solution import QueryBuilder


def test_select_columns():
    sql, params = QueryBuilder("users").select("id", "name").build()
    assert sql == "SELECT id, name FROM users"
    assert params == []


def test_multiple_where():
    sql, params = QueryBuilder("users").where("age", 18).where("active", True).build()
    assert sql == "SELECT * FROM users WHERE age = ? AND active = ?"
    assert params == [18, True]


def test_chained():
    sql, params = (
        QueryBuilder("orders")
        .select("id", "total")
        .where("status", "paid")
        .limit(5)
        .build()
    )
    assert sql == "SELECT id, total FROM orders WHERE status = ? LIMIT ?"
    assert params == ["paid", 5]
