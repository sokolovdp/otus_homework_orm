# Otus SQLite ORM homework project is an implementation of simple ORM. For SQL string generation is used package PYPIKA. 

##  To run test:
```
python orm_test.py
```

## Project is still in progress, current test results are:
```
2019-05-25 17:07:10,113 - ORM - INFO - Created connection <sqlite3.Connection object at 0x7fa053994570> with db_name: data.sqlite
2019-05-25 17:07:10,113 - ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
2019-05-25 17:07:10,113 - ORM - INFO - Schemas SQL: CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL;
2019-05-25 17:07:10,113 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test1', None, '2019-05-25 17:07:10.113796']
2019-05-25 17:07:10,114 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test2', None, '2019-05-25 17:07:10.114018']
2019-05-25 17:07:10,114 - ORM - INFO - UPDATE "users" SET "user_id"=76731,"username"='test1',"password"='password',"create_date"='2019-05-25 17:07:10.114156' WHERE "id"=76731
2019-05-25 17:07:10,114 - ORM - INFO - DELETE WHERE "users"."id"=76731
2019-05-25 17:07:10,114 - ORM - INFO - Closed connection <sqlite3.Connection object at 0x7fa053994570>
2019-05-25 17:07:10,114 - ORM - INFO - ORM stops,  stopped: 1 tables(s)
```
