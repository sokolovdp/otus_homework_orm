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
    ORM.start(db_file='data.sqlite')

    user1 = User(name='test1', password=None)
    user2 = User(name='test2', password=None)
    user3 = User(name='test3', password=None)
    user4 = User(name='test4', password=None)

    ORM.stop()

    pass
