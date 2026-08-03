from src.solution import QueryBuilder


def test_simple_select():
    sql, params = QueryBuilder("users").build()
    assert sql == "SELECT * FROM users"
    assert params == []


def test_where_parameterized():
    sql, params = QueryBuilder("users").where("age", 18).build()
    assert sql == "SELECT * FROM users WHERE age = ?"
    assert params == [18]


def test_limit_parameterized():
    sql, params = QueryBuilder("users").limit(10).build()
    assert sql == "SELECT * FROM users LIMIT ?"
    assert params == [10]


def test_user_value_never_interpolated():
    # A value that would be an injection if concatenated into the SQL text.
    malicious = "1 OR 1=1"
    sql, params = QueryBuilder("users").where("id", malicious).build()
    assert sql == "SELECT * FROM users WHERE id = ?"
    assert malicious not in sql
    assert params == [malicious]
