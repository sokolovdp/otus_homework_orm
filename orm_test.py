from sqlite_orm import fields, models, db_connector

db_connector.ORM.start(db_file='data.sqlite', generate_schemas=True)


class User(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='user_id')
    name = fields.StringField(max_length=80, db_field_name='username')
    password = fields.StringField(max_length=20, nullable=True)
    created = fields.DateTimeField(auto=True, db_field_name='create_date')

    class Meta:
        table = 'users'


if __name__ == "__main__":

    user = User(name='test', password=None)
    user.save()

    user.name = 'updated'
    user.update()
