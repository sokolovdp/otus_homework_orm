# Otus SQLite ORM homework project is an implementation of simple ORM. 

## For SQL string generation is used package *PYPIKA*.  

##  Basic ORM test:
```
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

```

## Test results are:
```
ORM - INFO - Created connection <sqlite3.Connection object at 0x7efec9ec78f0> with db_name: data.sqlite
ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
ORM - INFO - CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL, "group_id" INTEGER NOT NULL; CREATE TABLE IF NOT EXISTS  'groups' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "groupname" TEXT NOT NULL;
ORM - INFO - INSERT INTO "groups" ("group_id","groupname") VALUES (?,?): [None, 'group1']
ORM - INFO - UPDATE "groups" SET "group_id"=21017,"groupname"='group1-bis' WHERE "id"=21017
ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date","group_id") VALUES (?,?,?,?,?): [None, 'user1', None, '2019-05-28 00:00:36.550896', None]
ORM - INFO - UPDATE "users" SET "user_id"=69737,"username"='user1',"password"='password',"create_date"='2019-05-28 00:00:36.551021',"group_id"=21017 WHERE "id"=69737

ORM - INFO - SELECT * FROM "users" JOIN "group" ON "group_id" WHERE "users"."name"='dima' AND "users"."password"='test'

ORM - INFO - Closed connection <sqlite3.Connection object at 0x7efec9ec78f0>
ORM - INFO - ORM stops,  stopped: 2 table(s)
```
