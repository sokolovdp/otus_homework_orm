import logging
import os
import sqlite3
import sys

from .fields import DateTimeField, IntegerField, StringField

# from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type
# import pypika

# from .exceptions import OrmOperationalError, OrmConfigurationError


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
orm_logger = logging.getLogger('ORM')


class SqliteSchemaGenerator:
    TABLE_CREATE_TEMPLATE = "CREATE TABLE IF NOT EXISTS '{table_name}' ({fields} PRIMARY KEY {name});"
    FIELD_TEMPLATE = '"{name}" {db_type} {nullable}'

    FIELD_TYPE_MAP = {
        IntegerField: "INTEGER",
        StringField: "TEXT",
        DateTimeField: "TEXT",
    }


class SQLiteClient:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self._connection = None

    def open_connection(self, ):
        if not self._connection:
            self._connection = sqlite3.connect(self.db_file, isolation_level=None)
            self._connection.row_factory = sqlite3.Row
            orm_logger.info(f"Created connection {self._connection} with db_name: {self.db_file}")
            return self._connection

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            orm_logger.info(f"Closed connection {self._connection}")
            self._connection = None

    def db_create(self) -> None:
        pass

    def db_delete(self) -> None:
        self.close_connection()
        try:
            os.remove(self.db_file)
        except FileNotFoundError:
            pass
    #
    # def execute_query(self, query: str) -> List[dict]:
    #     with self.acquire_connection() as connection:
    #         self.log.debug(query)
    #         return [dict(row) for row in await connection.execute_fetchall(query)]
    #
    # def execute_script(self, query: str) -> None:
    #     with self.acquire_connection() as connection:
    #         self.log.debug(query)
    #         await connection.executescript(query)
    #
    # def execute_select(self, query, custom_fields: list = None) -> list:
    #     raw_results = self.db.execute_query(query.get_sql())
    #     instance_list = []
    #     for row in raw_results:
    #         instance = self.model(**row)
    #         if custom_fields:
    #             for field in custom_fields:
    #                 setattr(instance, field, row[field])
    #         instance_list.append(instance)
    #     return instance_list
    #
    # def _prepare_insert_columns(self) -> Tuple[List[str], List[str]]:
    #     regular_columns = []
    #     for column in self.model._meta.fields_db_projection.keys():
    #         field_object = self.model._meta.fields_map[column]
    #         if not field_object.generated:
    #             regular_columns.append(column)
    #     result_columns = [self.model._meta.fields_db_projection[c] for c in regular_columns]
    #     return regular_columns, result_columns
    #
    # def _prepare_insert_values(self, instance, regular_columns: List[str]) -> list:
    #     return [
    #         self._field_to_db(
    #             self.model._meta.fields_map[column], getattr(instance, column), instance
    #         )
    #         for column in regular_columns
    #     ]
    #
    #
    # def execute_insert(self, query: str, values: list) -> int:
    #     with self.acquire_connection() as connection:
    #         self.log.debug("%s: %s", query, values)
    #         return (connection.execute_insert(query, values))[0]
    #
    # def execute_insert2(self, instance):
    #     key = "{}:{}".format(self.db.connection_name, self.model._meta.table)
    #     if key not in INSERT_CACHE:
    #         regular_columns, columns = self._prepare_insert_columns()
    #         query = self._prepare_insert_statement(columns)
    #         INSERT_CACHE[key] = regular_columns, columns, query
    #     else:
    #         regular_columns, columns, query = INSERT_CACHE[key]
    #
    #     values = self._prepare_insert_values(instance=instance, regular_columns=regular_columns)
    #     instance.id = self.db.execute_insert(query, values)
    #     return instance
    #
    # def execute_update(self, instance):
    #     table = Table(self.model._meta.table)
    #     query = self.db.query_class.update(table)
    #     for field, db_field in self.model._meta.fields_db_projection.items():
    #         field_object = self.model._meta.fields_map[field]
    #         if not field_object.generated:
    #             query = query.set(
    #                 db_field, self._field_to_db(field_object, getattr(instance, field), instance)
    #             )
    #     query = query.where(table.id == instance.id)
    #     self.db.execute_query(query.get_sql())
    #     return instance
    #
    # def execute_delete(self, instance):
    #     table = Table(self.model._meta.table)
    #     query = self.model._meta.basequery.where(table.id == instance.id).delete()
    #     self.db.execute_query(query.get_sql())
    #     return instance
