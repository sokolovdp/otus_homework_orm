# Otus SQLite ORM homework project is an implementation of simple ORM. For SQL string generation is used package PYPIKA. 

##  To run test:
```
python orm_test.py
```

## Project is still in progress, current test results are:
```
ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
ORM - INFO - Schemas SQL: CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL;
ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test1', None, '2019-05-25 18:25:57.757098']
ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test2', None, '2019-05-25 18:25:57.757298']
ORM - INFO - UPDATE "users" SET "user_id"=416,"username"='test1',"password"='password',"create_date"='2019-05-25 18:25:57.757441' WHERE "id"=416
ORM - INFO - DELETE WHERE "users"."id"=416
ORM - INFO - SELECT * FROM "users" WHERE "name"='dima' AND "password"='test'
ORM - INFO - Closed connection <sqlite3.Connection object at 0x7fe9c98ba490>
ORM - INFO - ORM stops,  stopped: 1 table(s)
```
