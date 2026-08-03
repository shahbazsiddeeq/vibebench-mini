# src/solution.py

class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.params = []
        self.limit_value = None

    def select(self, *columns):
        if columns:
            self.columns = columns
        return self

    def where(self, column, value):
        self.conditions.append(f"{column} = ?")
        self.params.append(value)
        return self

    def limit(self, n):
        self.limit_value = n
        return self

    def build(self):
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        
        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)
        
        if self.limit_value is not None:
            sql += " LIMIT ?"
            self.params.append(self.limit_value)
        
        return sql, self.params
