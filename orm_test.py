from sqlite_orm import fields, models, db_connector

db_connector.ORM.start(db_file='data.sqlite', generate_schemas=True)


class User(models.OrmModel):
    id = fields.IntegerField(name='id', is_pk=True, db_field_name='user_id')
    name = fields.StringField(name='name', max_length=80, db_field_name='username')
    password = fields.StringField(name='password', max_length=20, nullable=True)
    created = fields.DateTimeField(name='created', auto=True, db_field_name='create_date')

    class Meta:
        table = 'users'


if __name__ == "__main__":

    user = User(name='test', password=None)

    print(User.__dict__)
    print(user.__dict__)

    user.save_to_db()

    user.update(name='updated')
    user.save_to_db()

    print(user.asdict())
