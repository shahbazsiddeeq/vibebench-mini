# src/solution.py

class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.params = []

    def select(self, *columns: str):
        if columns:
            self.columns = columns
        return self

    def where(self, column: str, value):
        self.conditions.append(f"{column} = ?")
        self.params.append(value)
        return self

    def limit(self, n: int):
        self.limit_value = n
        return self

    def build(self) -> tuple[str, list]:
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)
        if hasattr(self, 'limit_value'):
            sql += " LIMIT ?"
            self.params.append(self.limit_value)
        return sql, self.params
