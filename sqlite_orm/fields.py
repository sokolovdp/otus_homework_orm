from datetime import datetime
from typing import Any

MAX_STRING_LENGTH = 2000


class Field:
    def __init__(self, py_type, **kwargs):
        self.is_pk = kwargs.pop('is_pk', False)
        self.nullable = kwargs.pop('nullable', False)
        self.default = kwargs.pop('default', None)
        self.py_type = py_type
        self.db_field_name = kwargs.pop('db_field_name', None)
        self.max_length = kwargs.pop('max_length', None)
        self.auto_now = kwargs.pop('auto_now', False)

    def to_db_value(self, value: Any, instance) -> Any:
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
