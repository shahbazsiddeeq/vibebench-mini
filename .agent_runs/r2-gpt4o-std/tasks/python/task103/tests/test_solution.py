from src.solution import QueryBuilder


def test_simple_select():
    sql, params = QueryBuilder("users").build()
    assert sql == "SELECT * FROM users"
    assert params == []


def test_select_columns():
    sql, params = QueryBuilder("users").select("id", "name").build()
    assert sql == "SELECT id, name FROM users"
    assert params == []


def test_where_parameterized():
    sql, params = QueryBuilder("users").where("age", 18).build()
    assert sql == "SELECT * FROM users WHERE age = ?"
    assert params == [18]


def test_multiple_where():
    sql, params = QueryBuilder("users").where("age", 18).where("active", True).build()
    assert sql == "SELECT * FROM users WHERE age = ? AND active = ?"
    assert params == [18, True]


def test_limit_parameterized():
    sql, params = QueryBuilder("users").limit(10).build()
    assert sql == "SELECT * FROM users LIMIT ?"
    assert params == [10]


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


def test_user_value_never_interpolated():
    # A value that would be an injection if concatenated into the SQL text.
    malicious = "1 OR 1=1"
    sql, params = QueryBuilder("users").where("id", malicious).build()
    assert sql == "SELECT * FROM users WHERE id = ?"
    assert malicious not in sql
    assert params == [malicious]
