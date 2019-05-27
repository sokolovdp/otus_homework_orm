from sqlite_orm import fields, models, ORM


class User(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='user_id')
    name = fields.StringField(max_length=80, db_field_name='username')
    password = fields.StringField(max_length=20, nullable=True)
    created = fields.DateTimeField(auto_now=True, db_field_name='create_date')
    group = fields.ForeignKeyField("Group", related_name='groups')

    class Meta:
        db_table = 'users'
        safe_create = True  # create if not exists


class Group(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='group_id')
    name = fields.StringField(max_length=80, db_field_name='groupname')

    class Meta:
        db_table = 'groups'
        safe_create = True  # create if not exists


if __name__ == "__main__":
    ORM.start(db_file='data.sqlite')
    ORM.generate_schemas()

    # Create records for the model
    group1 = Group(name='group1')
    group1.save()

    group1.name = 'group1-bis'
    group1.save()

    # Create user and Fk to group
    user1 = User.create(name='user1', password=None)

    # Update record
    user1.password = 'password'
    user1.group_id = group1.id
    user1.save()

    # Select record(s)
    User.select('*', name='dima', password='test')

    ORM.stop()
