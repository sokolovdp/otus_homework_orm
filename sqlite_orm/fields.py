from datetime import datetime
from typing import Any

from sqlite_orm import exceptions

MAX_STRING_LENGTH = 2000
CASCADE = "CASCADE"
RESTRICT = "RESTRICT"
SET_NULL = "SET NULL"


class Field:
    def __init__(self, py_type, **kwargs):
        self.is_pk = kwargs.pop('is_pk', False)
        self.nullable = kwargs.pop('nullable', False)
        self.default = kwargs.pop('default', None)
        self.py_type = py_type
        self.db_field_name = kwargs.pop('db_field_name', None)
        self.max_length = kwargs.pop('max_length', None)
        self.auto_now = kwargs.pop('auto_now', False)
        self.unique = kwargs.pop('unique', False)
        self.model_field_name = ''

    def to_db_value(self, value: Any) -> Any:
        if value is None or type(value) == self.py_type:
            return value
        return self.py_type(value)

    def to_python_value(self, value: Any) -> Any:
        if value is None or isinstance(value, self.py_type):
            return value
        return self.py_type(value)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__(int, **kwargs)


class StringField(Field):
    def __init__(self, **kwargs):
        super().__init__(str, **kwargs)
        if not self.max_length:
            self.max_length = MAX_STRING_LENGTH


class DateTimeField(Field):
    def __init__(self, **kwargs):
        super().__init__(datetime, **kwargs)


class ForeignKeyField(Field):
    def __init__(self, model_name: str, related_name: str = None, on_delete: str = CASCADE, **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.related_name = related_name
        if on_delete not in {CASCADE, RESTRICT, SET_NULL}:
            raise exceptions.OrmConfigurationError("on_delete can only be CASCADE, RESTRICT or SET_NULL")
        if on_delete == SET_NULL and not bool(kwargs.get("nullable")):
            raise exceptions.OrmConfigurationError("If SET_NULL, then field must have nullable=True set")
        self.on_delete = on_delete


class ManyToManyField(Field):
    pass
