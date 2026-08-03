class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.params = []
        self._limit = None

    def select(self, *columns):
        self.columns = list(columns) if columns else ["*"]
        return self

    def where(self, column, value):
        self.conditions.append(f"{column} = ?")
        self.params.append(value)
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        params = list(self.params)

        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)

        if self._limit is not None:
            sql += " LIMIT ?"
            params.append(self._limit)

        return sql, params
