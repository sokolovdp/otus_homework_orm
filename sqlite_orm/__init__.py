import sys
import logging

from sqlite_orm import fields, models, exceptions

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

    @classmethod
    def _open_connection(cls, db_file: str = None):
        pass

    @classmethod
    def _start_models(cls, config: dict = None):
        pass

    @classmethod
    def _close_connection(cls, db_file: str = None):
        pass

    @classmethod
    def _stop_models(cls, config: dict = None):
        pass

    @classmethod
    def start(cls, db_file: str = 'data.sqlite',  create_db=False):
        cls._open_connection(db_file=db_file)
        cls._start_models()
        cls._started = True
        logger.info(f'started db_file: {db_file}   registered : {len(cls._all_models)} model(s)')

    @classmethod
    def stop(cls, db_file: str = 'data.sqlite', config: dict = None):
        cls._close_connection(db_file=db_file)
        cls._stop_models(config=config)
        cls._started = False
        logger.info(f'stopped')

    @classmethod
    def register_model(cls, model: models.OrmModel):
        cls._all_models.append(model)


