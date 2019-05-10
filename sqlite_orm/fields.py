from datetime import datetime

MAX_STRING_LENGTH = 2000


class Field:
    def __init__(self, py_type, **kwargs):
        self.is_pk = kwargs.pop('is_pk', False)
        self.nullable = kwargs.pop('nullable', False)
        self.default = kwargs.pop('default', None)
        self.py_type = py_type
        self.db_field_name = kwargs.pop('db_field_name', None)
        self.max_length = kwargs.pop('max_length', None)


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
