import sqlite3

from .exceptions import OrmOperationalError, OrmConfigurationError


class SQLite:

    @classmethod
    def get_connection(cls, bd_file: str = None):
        return 1
