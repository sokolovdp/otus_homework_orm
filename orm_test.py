from sqlite_orm import fields, models, ORM


class User(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='user_id')
    name = fields.StringField(max_length=80, db_field_name='username')
    password = fields.StringField(max_length=20, nullable=True)
    created = fields.DateTimeField(auto_now=True, db_field_name='create_date')

    class Meta:
        db_table = 'users'
        safe_create = True  # create if not exists


if __name__ == "__main__":
    ORM.start(db_file='data.sqlite')
    ORM.generate_schemas()

    # Create records for the model
    user1 = User(name='test1', password=None)
    user1.save()
    user2 = User.create(name='test2', password=None)

    # Update record
    user1.password = 'password'
    user1.save()

    # Delete record
    user1.delete()

    ORM.stop()
