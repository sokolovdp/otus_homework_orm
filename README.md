# Otus SQLite ORM homework project is an implementation of simple ORM. For SQL string generation is used package PYPIKA. 

##  Basic ORM test:
```
from sqlite_orm import fields, models, ORM


class User(models.OrmModel):
    id = fields.IntegerField(is_pk=True, db_field_name='user_id')
    name = fields.StringField(max_length=80, db_field_name='username')
    password = fields.StringField(max_length=20, nullable=True)
    created = fields.DateTimeField(auto_now=True, db_field_name='create_date')

    class Meta:
        db_table = 'users'
        safe_create = True  # create if not exists


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

# Select record(s)
User.select('*', name='dima', password='test')

ORM.stop()
```

## Current test results are:
```
ORM - INFO - Created connection <sqlite3.Connection object at 0x7fc2431bb570> with db_name: data.sqlite
ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
ORM - INFO - CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL;
ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test1', None, '2019-05-25 19:33:22.039187']
ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test2', None, '2019-05-25 19:33:22.039375']
ORM - INFO - UPDATE "users" SET "user_id"=34513,"username"='test1',"password"='password',"create_date"='2019-05-25 19:33:22.039458' WHERE "id"=34513
ORM - INFO - DELETE WHERE "users"."id"=34513
ORM - INFO - SELECT * FROM "users" WHERE "name"='dima' AND "password"='test'
ORM - INFO - Closed connection <sqlite3.Connection object at 0x7fc2431bb570>
ORM - INFO - ORM stops,  stopped: 1 table(s)
```
