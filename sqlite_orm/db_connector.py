import sqlite3

from .fields import IntegerField, StringField, DateTimeField

from .exceptions import OrmOperationalError, OrmConfigurationError


class BaseSchemaGenerator:
    TABLE_CREATE_TEMPLATE = "CREATE TABLE {exists} '{table_name}' ({fields});"
    FIELD_TEMPLATE = '"{name}" {db_type} {nullable}'

    FIELD_TYPE_MAP = {
        IntegerField: "BIGINT",
        StringField: "VARCHAR({})",
        DateTimeField: "TIMESTAMP",
    }


class SqliteSchemaGenerator(BaseSchemaGenerator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



class SQLite:

    @classmethod
    def get_connection(cls, bd_file: str = None):
        return 1
