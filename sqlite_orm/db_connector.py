import sqlite3
import random

from .exceptions import OrmOperationalError, OrmConfigurationError


class Executor:
    def __init__(self, orm):
        self.connection = orm.current_connection

    def execute_insert(self, table, *args, **kwargs):
        table.id = random.randint()
        return None

    def execute_update(self, table, *args, **kwargs):
        return None

    def execute_delete(self, table, *args, **kwargs):
        return None


class ORM:
    _connection = None
    _initiated = False

    @classmethod
    def start(cls, **kwargs):
        cls.db_name = kwargs.pop('db_name', 'data.sqlite')
        if kwargs.pop('generate_schemas', False):
            cls.generate_schemas()
        cls._connection = Executor(cls)
        cls._initiated = True

    @classmethod
    def generate_schemas(self):
        return None

    @classmethod
    @property
    def current_connection(self):
        return self._connection
