import logging
import os
import sqlite3
import sys
import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Iterable
from random import randint

from pypika import Parameter, Table, Query

from .fields import DateTimeField, IntegerField, StringField, Field
from .models import OrmModel, ModelInfo

# from .exceptions import OrmOperationalError, OrmConfigurationError


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
orm_logger = logging.getLogger('ORM')


def to_db_datetime(field_object, value: Optional[datetime.datetime], instance) -> Optional[str]:
    # if field_object.auto_now:
    #     value = datetime.datetime.utcnow()
    #     setattr(instance, field_object.model_field_name, value)
    #     return str(value)
    # if field_object.auto_now_add and getattr(instance, field_object.model_field_name) is None:
    #     value = datetime.datetime.utcnow()
    #     setattr(instance, field_object.model_field_name, value)
    #     return str(value)
    if isinstance(value, datetime.datetime):
        return str(value)
    return None


class SqliteSchema:
    TABLE_CREATE_TEMPLATE = "CREATE TABLE IF NOT EXISTS '{table_name}' ({fields} PRIMARY KEY {name});"
    FIELD_TEMPLATE = '"{name}" {db_type} {nullable}'
    FIELD_TYPE_MAP = {
        IntegerField: "INTEGER",
        StringField: "TEXT",
        DateTimeField: "TEXT",
    }


class SQLiteClient:
    TO_DB_OVERRIDE = {
        DateTimeField: to_db_datetime,
    }

    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.db_connection = None
        self.db_schema = SqliteSchema

    def open_connection(self) -> Any:
        if not self.db_connection:
            self.db_connection = sqlite3.connect(self.db_file, isolation_level=None)
            self.db_connection.row_factory = sqlite3.Row
            orm_logger.info(f"Created connection {self.db_connection} with db_name: {self.db_file}")
            return self.db_connection

    def close_connection(self) -> None:
        if self.db_connection:
            self.db_connection.close()
            orm_logger.info(f"Closed connection {self.db_connection}")
            self.db_connection = None

    def db_create(self) -> None:
        pass

    def db_delete(self) -> None:
        self.close_connection()
        try:
            os.remove(self.db_file)
        except FileNotFoundError:
            pass

    @classmethod
    def _field_to_db(cls, field_object: Field, attr: Any, instance) -> Any:
        if field_object.__class__ in cls.TO_DB_OVERRIDE:
            return cls.TO_DB_OVERRIDE[field_object.__class__](field_object, attr, instance)
        return field_object.to_db_value(attr, instance)

    def _run_insert(self, sql, values) -> Optional[Iterable[sqlite3.Row]]:
        orm_logger.info("%s: %s", sql, values)
        # self.db_connection.
        return randint(1, 100000)  # TODO DEBUG

    def _run_query(self, sql: str) -> List[dict]:
        orm_logger.info("%s: %s", sql)
        result = [dict(row) for row in self.db_connection.execute_fetchall(sql)]
        return result

    def _prepare_insert_columns(self, instance) -> Tuple[List[str], List[str]]:
        model_columns = instance._meta.fields_db.keys()
        db_columns = [instance._meta.fields_db[c] for c in model_columns]
        return model_columns, db_columns

    def _prepare_insert_statement(self, instance, db_columns: List[str]) -> str:
        return str(
            Query.into(Table(instance._meta.db_table))
                .columns(*db_columns)
                .insert(*[Parameter("?") for _ in range(len(db_columns))])
        )

    def _prepare_insert_values(self, instance=None, model_columns: List[str] = None) -> list:
        return [
            self._field_to_db(instance._meta.fields_map[column], getattr(instance, column), instance)
            for column in model_columns
        ]

    def execute_insert(self, instance: OrmModel, **kwargs) -> OrmModel:
        model_columns, db_columns = self._prepare_insert_columns(instance)
        query = self._prepare_insert_statement(instance, db_columns)
        values = self._prepare_insert_values(instance=instance, model_columns=model_columns)
        instance.id = self._run_insert(query, values)
        return instance

    def execute_update(self, instance, **kwargs):
        db_table = Table(instance._meta.db_table)
        query = Query.update(db_table)
        for field, db_field in instance._meta.fields_db_projection.items():
            field_object = instance._meta.fields_map[field]
            query = query.set(db_field, self._field_to_db(field_object, getattr(instance, field), instance))
        query = query.where(db_table.id == instance.id)
        self.db.execute_query(query.get_sql())
        return instance

    def execute_delete(self, instance, **kwargs):
        table = Table(instance._meta.table)
        query = instance._meta.basequery.where(table.id == instance.id).delete()
        self._run_query(query.get_sql())
        return instance

    # def _run_select(self, query, custom_fields: list = None) -> list:
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
