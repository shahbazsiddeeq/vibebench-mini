# src/solution.py

from typing import List, Tuple

class QueryBuilder:
    def __init__(self, table: str):
        if not isinstance(table, str) or not table.isidentifier():
            raise ValueError("Invalid table name.")
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.params = []
        self.limit_value = None

    def select(self, *columns: str):
        if not all(isinstance(col, str) and col.isidentifier() for col in columns):
            raise ValueError("Invalid column names.")
        if columns:
            self.columns = columns
        return self

    def where(self, column: str, value):
        if not isinstance(column, str) or not column.isidentifier():
            raise ValueError("Invalid column name.")
        self.conditions.append(f"{column} = ?")
        self.params.append(value)
        return self

    def limit(self, n: int):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Limit must be a positive integer.")
        self.limit_value = n
        return self

    def build(self) -> Tuple[str, List]:
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)
        if self.limit_value is not None:
            sql += " LIMIT ?"
            self.params.append(self.limit_value)
        return sql, self.params
