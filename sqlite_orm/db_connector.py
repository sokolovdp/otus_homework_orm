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

from .exceptions import OrmOperationalError, OrmConfigurationError


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
orm_logger = logging.getLogger('ORM')


def to_db_datetime(field_object, value: Optional[datetime.datetime], instance) -> Optional[str]:
    if field_object.auto_now:
        value = datetime.datetime.now()
        setattr(instance, field_object.model_field_name, value)
        return str(value)
    if isinstance(value, datetime.datetime):
        return str(value)
    return None


class SqliteSchema:
    TABLE_CREATE_TEMPLATE = "CREATE TABLE {exists} '{table_name}' ({fields};"
    FIELD_TEMPLATE = '"{name}" {db_type} {nullable} {unique}'
    FIELD_TYPE_MAP = {
        IntegerField: "INTEGER",
        StringField: "TEXT",
        DateTimeField: "TEXT",
    }
    PRIMARY_FIELD_CREATE_TEMPLATE = '"{}" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'
    UNIQUE_CREATE_TEMPLATE = "UNIQUE ({fields})"
    NULLABLE = "NOT NULL"
    UNIQUE = "UNIQUE"

    def __init__(self, client) -> None:
        self.client = client

    def get_field_string(self, db_field: str, field_type: str, nullable: str, unique: str) -> str:
        field_creation_string = self.FIELD_TEMPLATE.format(
            name=db_field,
            db_type=field_type,
            nullable=nullable,
            unique=unique
        ).strip()
        return field_creation_string

    def get_primary_key_string(self, field_name: str) -> str:
        return self.PRIMARY_FIELD_CREATE_TEMPLATE.format(field_name)

    def get_unique_string(self, field_names: List[str]) -> str:
        return self.UNIQUE_CREATE_TEMPLATE.format(fields=", ".join(field_names))

    def get_table_sql(self, model) -> str:
        fields_to_create = []
        for field_name, db_field in model.model_meta.fields_db.items():
            field_object = model.model_meta.fields_map[field_name]
            if isinstance(field_object, IntegerField) and field_object.is_pk:
                fields_to_create.append(self.get_primary_key_string(field_name))
                continue
            nullable = self.NULLABLE if not field_object.nullable else ""
            unique = self.UNIQUE if field_object.unique else ""

            field_object_type = type(field_object)
            while field_object_type.__bases__ and field_object_type not in self.FIELD_TYPE_MAP:
                field_object_type = field_object_type.__bases__[0]

            field_type = self.FIELD_TYPE_MAP[field_object_type]
            field_creation_string = self.get_field_string(db_field, field_type, nullable, unique)
            fields_to_create.append(field_creation_string)

        table_fields_string = ", ".join(fields_to_create)
        table_create_string = self.TABLE_CREATE_TEMPLATE.format(
            exists="IF NOT EXISTS " if model.model_meta.safe_create else "",
            table_name=model.model_meta.db_table,
            fields=table_fields_string,
        )
        return table_create_string

    def get_create_schema_sql(self) -> str:
        import sqlite_orm
        models_to_create = []

        for model in sqlite_orm.ORM.all_tables.values():
            models_to_create.append(model)

        tables_to_create = []
        for model in models_to_create:
            tables_to_create.append(self.get_table_sql(model))

        schema_creation_string = " ".join(tables_to_create)
        return schema_creation_string

    def create_schemas(self):
        create_schemas_sql = self.get_create_schema_sql()
        orm_logger.info(f"Schemas SQL: {create_schemas_sql}")
        # run sql str


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
        orm_logger.info("%s", sql)
        # result = [dict(row) for row in self.db_connection.execute_fetchall(sql)]
        return None  # TODO DEBUG

    def _prepare_insert_columns(self, instance) -> Tuple[List[str], List[str]]:
        model_columns = instance.model_meta.fields_db.keys()
        db_columns = [instance.model_meta.fields_db[c] for c in model_columns]
        return model_columns, db_columns

    def _prepare_insert_statement(self, instance, db_columns: List[str]) -> str:
        return str(
            Query.into(Table(instance.model_meta.db_table))
                .columns(*db_columns)
                .insert(*[Parameter("?") for _ in range(len(db_columns))])
        )

    def _prepare_insert_values(self, instance=None, model_columns: List[str] = None) -> list:
        return [
            self._field_to_db(instance.model_meta.fields_map[column], getattr(instance, column), instance)
            for column in model_columns
        ]

    def execute_insert(self, instance: OrmModel, **kwargs) -> OrmModel:
        model_columns, db_columns = self._prepare_insert_columns(instance)
        query = self._prepare_insert_statement(instance, db_columns)
        values = self._prepare_insert_values(instance=instance, model_columns=model_columns)
        instance.id = self._run_insert(query, values)
        return instance

    def execute_update(self, instance, **kwargs):
        db_table = Table(instance.model_meta.db_table)
        query = Query.update(db_table)
        for field, db_field in instance.model_meta.fields_db.items():
            field_object = instance.model_meta.fields_map[field]
            query = query.set(db_field, self._field_to_db(field_object, getattr(instance, field), instance))
        query = query.where(db_table.id == instance.id)
        self._run_query(query.get_sql())
        return instance

    def execute_delete(self, instance, **kwargs):
        db_table = Table(instance.model_meta.db_table)
        query = instance.model_meta.basequery.where(db_table.id == instance.id).delete()
        self._run_query(query.get_sql())
        return instance

    def execute_select(self, instance, custom_fields: list = None) -> list:
        instance_list = []
        # db_table = Table(instance.model_meta.db_table)
        # raw_results = self.db.execute_query(query.get_sql())
        # for row in raw_results:
        #     instance = self.model(**row)
        #     if custom_fields:
        #         for field in custom_fields:
        #             setattr(instance, field, row[field])
        #     instance_list.append(instance)
        return instance_list

