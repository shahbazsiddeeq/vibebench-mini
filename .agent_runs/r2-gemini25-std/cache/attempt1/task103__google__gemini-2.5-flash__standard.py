class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._columns = ["*"]
        self._where_conditions = []
        self._params = []
        self._limit = None

    def select(self, *columns) -> "QueryBuilder":
        if columns:
            self._columns = list(columns)
        return self

    def where(self, column: str, value) -> "QueryBuilder":
        self._where_conditions.append(f"{column} = ?")
        self._params.append(value)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> tuple[str, list]:
        sql_parts = []
        current_params = []

        # SELECT clause
        sql_parts.append(f"SELECT {', '.join(self._columns)}")

        # FROM clause
        sql_parts.append(f"FROM {self._table}")

        # WHERE clause
        if self._where_conditions:
            sql_parts.append(f"WHERE {' AND '.join(self._where_conditions)}")
            current_params.extend(self._params)

        # LIMIT clause
        if self._limit is not None:
            sql_parts.append("LIMIT ?")
            current_params.append(self._limit)

        return " ".join(sql_parts), current_params
