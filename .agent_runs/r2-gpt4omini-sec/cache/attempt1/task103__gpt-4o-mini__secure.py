# src/solution.py

class QueryBuilder:
    def __init__(self, table: str):
        if not isinstance(table, str) or not table.isidentifier():
            raise ValueError("Invalid table name.")
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.limit_value = None

    def select(self, *columns: str):
        if not columns:
            self.columns = ["*"]
        else:
            for column in columns:
                if not isinstance(column, str) or not column.isidentifier():
                    raise ValueError(f"Invalid column name: {column}")
            self.columns = list(columns)
        return self

    def where(self, column: str, value):
        if not isinstance(column, str) or not column.isidentifier():
            raise ValueError(f"Invalid column name: {column}")
        self.conditions.append((column, value))
        return self

    def limit(self, n: int):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Limit must be a non-negative integer.")
        self.limit_value = n
        return self

    def build(self) -> tuple[str, list]:
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        params = []

        if self.conditions:
            condition_clauses = []
            for column, value in self.conditions:
                condition_clauses.append(f"{column} = ?")
                params.append(value)
            sql += " WHERE " + " AND ".join(condition_clauses)

        if self.limit_value is not None:
            sql += " LIMIT ?"
            params.append(self.limit_value)

        return sql, params
