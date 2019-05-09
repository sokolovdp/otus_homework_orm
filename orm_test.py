from datetime import datetime
from sqlite_orm import fields, models, ORM


class User(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='user_id')
    name = fields.StringField(max_length=80, db_field_name='username')
    password = fields.StringField(max_length=20, nullable=True)
    created = fields.DateTimeField(default=datetime.today(), db_field_name='create_date')

    class Meta:
        table = 'users'


if __name__ == "__main__":

    user = User(name='test', password=None)
    config = {'models': ['__main__', ]}

    ORM.start(db_file='data.sqlite', config=config, create_db=True)

    ORM.stop()

