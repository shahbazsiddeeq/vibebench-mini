import collections
import copy
import secrets


class MemDB:
    """
    An in-memory database for storing and querying dictionary-like rows.

    This class provides basic CRUD operations (Create, Read, Delete) on
    named tables. It prioritizes security by validating inputs, avoiding
    unsafe operations, and handling errors gracefully without exposing
    internal details.
    """

    def __init__(self):
        """
        Initializes an empty in-memory database.
        The database stores tables as dictionaries, where each table
        is a list of rows (dictionaries).
        """
        self._data = collections.defaultdict(list)

    def _validate_table_name(self, table):
        """
        Validates the table name.

        Args:
            table: The table name to validate.

        Raises:
            ValueError: If the table name is not a non-empty string.
        """
        if not isinstance(table, str) or not table:
            raise ValueError("Table name must be a non-empty string.")

    def _validate_row(self, row):
        """
        Validates a row to be inserted.

        Args:
            row: The row (dictionary) to validate.

        Raises:
            ValueError: If the row is not a dictionary.
        """
        if not isinstance(row, dict):
            raise ValueError("Row must be a dictionary.")
        # Further validation could be added here, e.g., checking for valid keys/values
        # For this task, we assume dictionary values are safe to store.

    def _validate_filters(self, filters):
        """
        Validates the filters.

        Args:
            filters: The filters (keyword arguments) to validate.

        Raises:
            ValueError: If any filter key is not a string.
        """
        for key in filters:
            if not isinstance(key, str):
                raise ValueError("Filter keys must be strings.")

    def insert(self, table: str, row: dict):
        """
        Inserts a new row into the specified table.

        Args:
            table: The name of the table to insert into.
            row: The dictionary representing the row to insert.

        Raises:
            ValueError: If table name or row is invalid.
        """
        self._validate_table_name(table)
        self._validate_row(row)

        # Store a deep copy of the row to prevent external modification
        # of the stored data.
        try:
            self._data[table].append(copy.deepcopy(row))
        except TypeError as e:
            # Catch potential issues with uncopyable objects in the row
            raise ValueError(f"Row contains uncopyable elements: {e}") from e

    def find(self, table: str, **filters) -> list[dict]:
        """
        Finds rows in the specified table that match all provided filters.

        Args:
            table: The name of the table to search.
            **filters: Keyword arguments representing the filter conditions.
                       Only rows where all filter key-value pairs match
                       will be returned. If no filters are provided, all
                       rows in the table are returned.

        Returns:
            A list of dictionaries, where each dictionary is a deep copy
            of a matching row. Returns an empty list if the table does
            not exist or no rows match.

        Raises:
            ValueError: If table name or filters are invalid.
        """
        self._validate_table_name(table)
        self._validate_filters(filters)

        if table not in self._data:
            return []

        results = []
        for row in self._data[table]:
            match = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    match = False
                    break
            if match:
                # Return a deep copy of the row to prevent external modification
                try:
                    results.append(copy.deepcopy(row))
                except TypeError as e:
                    # This should ideally not happen if insert already deepcopies,
                    # but as a defensive measure.
                    raise RuntimeError(f"Failed to copy row during find operation: {e}") from e
        return results

    def delete(self, table: str, **filters) -> int:
        """
        Deletes rows from the specified table that match all provided filters.

        Args:
            table: The name of the table to delete from.
            **filters: Keyword arguments representing the filter conditions.
                       Only rows where all filter key-value pairs match
                       will be deleted. If no filters are provided, all
                       rows in the table are deleted.

        Returns:
            The number of rows deleted.

        Raises:
            ValueError: If table name or filters are invalid.
        """
        self._validate_table_name(table)
        self._validate_filters(filters)

        if table not in self._data:
            return 0

        original_count = len(self._data[table])
        new_rows = []
        deleted_count = 0

        for row in self._data[table]:
            match = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    match = False
                    break
            if not match:
                new_rows.append(row)
            else:
                deleted_count += 1

        self._data[table] = new_rows
        return deleted_count
