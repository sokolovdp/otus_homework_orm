from collections import defaultdict
from sqlite_orm import fields, models, exceptions, db_connector
from .db_connector import orm_logger

__all__ = ['ORM', 'fields', 'models', 'exceptions']


class ORM:
    _started = False
    _all_models = []
    _all_tables = defaultdict(models.ModelInfo)
    _db_connection = None
    db_client = None

    @classmethod
    def _create_connection(cls, bd_client, db_file: str = None, create_db=False):
        if bd_client == 'sqlite':
            if not create_db:
                cls.db_client = db_connector.SQLiteClient(db_file=db_file)
                cls._db_connection = cls.db_client.open_connection()
        else:
            raise exceptions.OrmConfigurationError('Only SQLite DB connection is implemented')

    @classmethod
    def _start_models(cls):
        for model in cls._all_models:
            model._meta.db_connection = cls._db_connection
            model._meta.started = True

    @classmethod
    def _delete_connection(cls):
        cls.db_client.close_connection()

    @classmethod
    def _stop_models(cls):
        for model in cls._all_models:
            model._meta.db_connection = None
            model._meta.started = False

    @classmethod
    def start(cls, db_file: str = 'data.sqlite',  create_db=False):
        cls._create_connection('sqlite', db_file=db_file, create_db=create_db)
        cls._start_models()
        cls._started = True
        orm_logger.info(f'ORM started, client: SQLite3,  db_file: {db_file}')

    @classmethod
    def stop(cls):
        cls._delete_connection()
        cls._stop_models()
        cls._started = False
        orm_logger.info(f'ORM stops,  stopped: {len(cls._all_models)} model(s)')

    @classmethod
    def register_model(cls, model: models.OrmModel):
        model._meta.db_connection = cls._db_connection
        model._meta.db_client = cls.db_client
        model._meta.started = cls._started
        cls._all_models.append(model)

    @classmethod
    def register_table(cls, table: models.ModelInfo):
        cls._all_tables[table.db_table] = table

