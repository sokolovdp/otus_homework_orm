from sqlite_orm import db_connector, exceptions, fields, models
from .db_connector import orm_logger

__all__ = ['ORM', 'fields', 'models', 'exceptions']


class ORM:
    started = False
    all_tables = dict()
    db_connection = None
    db_client = None
    db_schema = None

    @classmethod
    def _create_connection(cls, bd_client, db_file: str = None, create_db=False):
        if bd_client == 'sqlite':
            if not create_db:
                cls.db_client = db_connector.SQLiteClient(db_file=db_file)
                cls.db_connection = cls.db_client.open_connection()
                cls.db_schema = db_connector.SqliteSchema(cls.db_client)
        else:
            raise exceptions.OrmConfigurationError('Only SQLite DB connection is implemented')

    @classmethod
    def _delete_connection(cls):
        cls.db_client.close_connection()
        cls.db_client = None
        cls.db_connection = None

    @classmethod
    def register_model(cls, model: models.OrmModel):
        model.model_meta.db_client = cls.db_client
        model.model_meta.started = cls.started

    # @classmethod
    # def _register_table(cls, table: type):
    #     cls.all_tables.append(table)

    @classmethod
    def start(cls, db_file: str = 'data.sqlite', create_db=False):
        cls._create_connection('sqlite', db_file=db_file, create_db=create_db)
        cls.started = True
        orm_logger.info(f'ORM started, client: SQLite3,  db_file: {db_file}')

    @classmethod
    def stop(cls):
        cls._delete_connection()
        cls.started = False
        orm_logger.info(f'ORM stops,  stopped: {len(cls.all_tables)} table(s)')

    @classmethod
    def generate_schemas(cls):
        if len(models.ALL_ORM_TABLES) < 2:
            raise exceptions.OrmOperationalError('No registered tables!')
        for table in models.ALL_ORM_TABLES[1:]:
            if table.model_meta.db_table in cls.all_tables.keys():
                raise exceptions.OrmConfigurationError(f'Duplicated schema: {table.model_meta.db_table}')
            else:
                cls.all_tables[table.model_meta.db_table] = table
        cls.db_schema.create_schemas()
