from sqlite_orm import fields, models, exceptions, db_connector
from .db_connector import orm_logger

__all__ = ['ORM', 'fields', 'models', 'exceptions']


class ORM:
    _started = False
    _all_models = []
    _db_connection = None
    _db_client = None

    @classmethod
    def _create_connection(cls, bd_client, db_file: str = None, create_db=False):
        if bd_client == 'sqlite':
            if not create_db:
                cls._db_client = db_connector.SQLiteClient(db_file=db_file)
                cls._db_connection = cls._db_client.open_connection()
        else:
            raise exceptions.OrmConfigurationError('Only SQLite DB connection is implemented')

    @classmethod
    def _start_models(cls):
        for model in cls._all_models:
            model._meta.db_connection = cls._db_connection
            model._meta.started = True

    @classmethod
    def _delete_connection(cls):
        cls._db_client.close_connection()

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
        orm_logger.info(f'ORM started db_file: {db_file}   registered : {len(cls._all_models)} model(s)')

    @classmethod
    def stop(cls):
        cls._delete_connection()
        cls._stop_models()
        cls._started = False
        orm_logger.info(f'ORM stopped')

    @classmethod
    def register_model(cls, model: models.OrmModel):
        cls._all_models.append(model)


