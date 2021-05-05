import sqlite3
from typing import Any, Dict, Iterable, Optional


class DBInteractor:
    def __init__(self, db_filename: str):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(
        self, statement: str, values: Optional[Iterable[str]] = None
    ) -> sqlite3.Cursor:
        parameters = values if values is not None else []

        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            return cursor

    def create_db(
        self, table_name: str, column_definitions: Dict[str, str]
    ) -> None:
        columns = ", ".join(
            [
                f"{column_name} {column_definition}"
                for column_name, column_definition in column_definitions.items()
            ]
        )

        statement = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
        """

        self._execute(statement)

    def add(self, table_name: str, data: Dict[str, Any]) -> None:
        value_placeholders = ", ".join(["?"] * len(data))
        fields = ", ".join(data.keys())
        values = tuple(data.values())

        statement = f"""
        INSERT INTO {table_name} (
            {fields}
        ) VALUES (
            {value_placeholders}
        )
        """

        self._execute(statement, values)

    def delete(self, table_name: str, filters: Dict[str, Any]) -> None:
        value_placeholders = " AND ".join(
            [f"{column} = ?" for column in filters.keys()]
        )
        values = tuple(filters.values())

        statement = f"""
        DELETE FROM {table_name}
        WHERE {value_placeholders}
        """

        self._execute(statement, values)

    def get(
        self,
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> sqlite3.Cursor:
        if filters is None:
            filters = {}

        values_placeholders = " AND ".join(
            [f"{column} = ?" for column in filters.keys()]
        )
        values = tuple(filters.values())

        statement = f"""
        SELECT * FROM {table_name}
        """

        if filters:  # checking if dict is not empty
            statement += f"""
            WHERE {values_placeholders}
            """

        if order_by:  # checking if not None and not empty string
            statement += f"""
            ORDER BY {order_by}
            """

        return self._execute(statement, values)
