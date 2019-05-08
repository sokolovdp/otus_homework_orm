from datetime import datetime

from .exceptions import OrmOperationalError, OrmConfigurationError

MAX_STRING_LENGTH = 4000


class Field:

    def __init__(self, name, py_type, **kwargs):
        if self.__class__ is Field:
            raise TypeError("'Field' is internal abstract type")
        self.name = name
        self.is_pk = kwargs.pop('is_pk', False)
        self.nullable = kwargs.pop('nullable', False)
        self.auto = kwargs.pop('auto', False)
        self.py_type = py_type
        self.db_field_name = kwargs.pop('db_field_name', None)
        self.max_length = kwargs.pop('max_length', None)
        self.value = None


class IntegerField(Field):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, int, **kwargs)


class StringField(Field):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, str, **kwargs)
        if self.max_length:
            try:
                if int(self.max_length) < 1:
                    raise OrmConfigurationError("'max_length' must be >= 1")
            except ValueError:
                raise OrmConfigurationError("'max_length' must be positive int >= 1")
        else:
            self.max_length = MAX_STRING_LENGTH


class DateTimeField(Field):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, datetime, **kwargs)
