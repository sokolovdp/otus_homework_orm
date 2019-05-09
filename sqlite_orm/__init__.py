import sys
import logging

from sqlite_orm import fields, models, exceptions, db_connector

__all__ = ['ORM', 'fields', 'models', 'exceptions']

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ORM')


class ORM:
    _started = False
    _all_models = []
    _db_connection = None

    @classmethod
    def _open_connection(cls, bd: str, db_file: str = None):
        if bd == 'sqlite':
            connection = db_connector.SQLite.get_connection(bd_file=db_file)
        else:
            raise exceptions.OrmConfigurationError('Only SQLite DB connection is implemented')
        return connection

    @classmethod
    def _start_models(cls):
        for model in cls._all_models:
            model._meta.db_connection = cls._db_connection
            model._meta.started = True

    @classmethod
    def _close_connection(cls):
        pass

    @classmethod
    def _stop_models(cls):
        pass

    @classmethod
    def start(cls, db_file: str = 'data.sqlite',  create_db=False):
        cls._db_connection = cls._open_connection('sqlite', db_file=db_file)
        cls._start_models()
        cls._started = True
        logger.info(f'started db_file: {db_file}   registered : {len(cls._all_models)} model(s)')

    @classmethod
    def stop(cls):
        cls._close_connection()
        cls._stop_models()
        cls._started = False
        logger.info(f'stopped')

    @classmethod
    def register_model(cls, model: models.OrmModel):
        cls._all_models.append(model)


