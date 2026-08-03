import re

class QueryBuilder:
    def __init__(self, table: str):
        if not isinstance(table, str) or not table:
            raise ValueError("Table name must be a non-empty string.")
        if not re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table):
            raise ValueError("Invalid table name format.")
        self._table = table
        self._columns = ["*"]
        self._where_conditions = []
        self._params = []
        self._limit = None

    def select(self, *columns: str) -> "QueryBuilder":
        if not columns:
            self._columns = ["*"]
        else:
            validated_columns = []
            for col in columns:
                if not isinstance(col, str) or not col:
                    raise ValueError("Column names must be non-empty strings.")
                if not re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.]*$", col):
                    raise ValueError(f"Invalid column name format: {col}")
                validated_columns.append(col)
            self._columns = validated_columns
        return self

    def where(self, column: str, value: any) -> "QueryBuilder":
        if not isinstance(column, str) or not column:
            raise ValueError("Column name for WHERE clause must be a non-empty string.")
        if not re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.]*$", column):
            raise ValueError(f"Invalid column name format for WHERE clause: {column}")
        self._where_conditions.append(f"{column} = ?")
        self._params.append(value)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Limit must be a positive integer.")
        self._limit = n
        return self

    def build(self) -> tuple[str, list]:
        sql_parts = [f"SELECT {', '.join(self._columns)} FROM {self._table}"]
        current_params = list(self._params) # Make a copy for this build call

        if self._where_conditions:
            sql_parts.append(f"WHERE {' AND '.join(self._where_conditions)}")

        if self._limit is not None:
            sql_parts.append("LIMIT ?")
            current_params.append(self._limit)

        return " ".join(sql_parts), current_params
