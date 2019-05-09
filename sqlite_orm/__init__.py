import sys
import logging

from sqlite_orm import fields, models

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ORM')


class ORM:
    _started = False

    @classmethod
    def open_connection(cls, db_file: str = None):
        pass

    @classmethod
    def start_models(cls, config: dict = None):
        pass

    @classmethod
    def start(cls, db_file: str = 'data.sqlite', config: dict = None):
        cls.open_connection(db_file=db_file)
        cls.start_models(config=config)
        cls._started = True
        logger.info(f'started db_file: {db_file}   config: {str(config)}')

    @classmethod
    def close_connection(cls, db_file: str = None):
        pass

    @classmethod
    def stop_models(cls, config: dict = None):
        pass

    @classmethod
    def stop(cls, db_file: str = 'data.sqlite', config: dict = None):
        cls.close_connection(db_file=db_file)
        cls.stop_models(config=config)
        cls._started = False
        logger.info(f'stopped')
