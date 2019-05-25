# Otus SQLite ORM homework project is an implementation of simple ORM. For SQL string generation is used package PYPIKA. 

##  To run test:
```
python orm_test.py
```

## Project is still in progress, current test results are:
```
2019-05-25 14:13:51,341 - ORM - INFO - Created connection <sqlite3.Connection object at 0x7f7bbf2139d0> with db_name: data.sqlite
2019-05-25 14:13:51,341 - ORM - INFO - ORM started, client: SQLite3,  db_file: data.sqlite
2019-05-25 14:13:51,341 - ORM - INFO - Schemas SQL: CREATE TABLE IF NOT EXISTS  'users' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL; CREATE TABLE IF NOT EXISTS  'users2' ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "username" TEXT NOT NULL, "password" TEXT, "create_date" TEXT NOT NULL;
2019-05-25 14:13:51,341 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test1', None, '2019-05-25 14:13:51.341851']
2019-05-25 14:13:51,342 - ORM - INFO - INSERT INTO "users" ("user_id","username","password","create_date") VALUES (?,?,?,?): [None, 'test3', None, '2019-05-25 14:13:51.341989']
2019-05-25 14:13:51,342 - ORM - INFO - Closed connection <sqlite3.Connection object at 0x7f7bbf2139d0>
2019-05-25 14:13:51,342 - ORM - INFO - ORM stops,  stopped: 2 tables(s)
```
