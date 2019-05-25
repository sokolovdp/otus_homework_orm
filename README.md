# Otus SQLite ORM homework project is an implementation of simple ORM. For SQL string generation is used package PYPIKA. 

##  To run test:
```
python orm_test.py
```

## Project is still in progress, current test results are:
```
2019-05-25 17:03:29,910 - ORM - INFO - Created connection <sqlite3.Connection object at 0x7fb972518570> with db_name: data.sqlite
2019-05-25 17:03:29,910 - ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
2019-05-25 17:03:29,910 - ORM - INFO - Schemas SQL: CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL;
2019-05-25 17:03:29,910 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test1', None, '2019-05-25 17:03:29.910605']
2019-05-25 17:03:29,910 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test2', None, '2019-05-25 17:03:29.910734']
2019-05-25 17:03:29,910 - ORM - INFO - DELETE WHERE "users"."id"=59892
2019-05-25 17:03:29,910 - ORM - INFO - Closed connection <sqlite3.Connection object at 0x7fb972518570>
2019-05-25 17:03:29,910 - ORM - INFO - ORM stops,  stopped: 1 tables(s)
```
