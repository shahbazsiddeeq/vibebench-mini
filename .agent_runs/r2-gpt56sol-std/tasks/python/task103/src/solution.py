from typing import Any


class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.columns: tuple[str, ...] = ()
        self.conditions: list[tuple[str, Any]] = []
        self.row_limit: Any = None
        self._has_limit = False

    def select(self, *columns: str) -> "QueryBuilder":
        self.columns = columns
        return self

    def where(self, column: str, value: Any) -> "QueryBuilder":
        self.conditions.append((column, value))
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self.row_limit = n
        self._has_limit = True
        return self

    def build(self) -> tuple[str, list[Any]]:
        selected = ", ".join(self.columns) if self.columns else "*"
        sql = f"SELECT {selected} FROM {self.table}"
        params: list[Any] = []

        if self.conditions:
            sql += " WHERE " + " AND ".join(
                f"{column} = ?" for column, _ in self.conditions
            )
            params.extend(value for _, value in self.conditions)

        if self._has_limit:
            sql += " LIMIT ?"
            params.append(self.row_limit)

        return sql, params
