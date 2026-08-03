"""In-memory database module."""

from collections import defaultdict


class MemDB:
    """A simple in-memory database supporting multiple tables."""

    def __init__(self):
        self._tables = defaultdict(list)

    def insert(self, table, row):
        """Insert a row (dict) into the given table."""
        self._tables[table].append(dict(row))

    def find(self, table, **filters):
        """Return list of rows matching all filters (AND)."""
        rows = self._tables.get(table, [])
        if not filters:
            return [dict(row) for row in rows]
        result = []
        for row in rows:
            if all(row.get(k) == v for k, v in filters.items()):
                result.append(dict(row))
        return result

    def delete(self, table, **filters):
        """Delete rows matching all filters (AND), return count deleted."""
        rows = self._tables.get(table, [])
        if not filters:
            count = len(rows)
            self._tables[table] = []
            return count

        remaining = []
        count = 0
        for row in rows:
            if all(row.get(k) == v for k, v in filters.items()):
                count += 1
            else:
                remaining.append(row)
        self._tables[table] = remaining
        return count
