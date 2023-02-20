
>>> import sqlite3

>>> sqliteConnection  = sqlite3.connect("src/mazes/mazes_app.db")

>>> sqliteConnection
<sqlite3.Connection object at 0x00000198DAA8A8A0>


>>> cursor = sqliteConnection.cursor()


>>> all_tables_query = """SELECT name FROM sqlite_master WHERE type='table';"""

>>> all_tables_query
>
"SELECT name FROM sqlite_master WHERE type='table';"


>>> cursor.execute(all_tables_query)
<sqlite3.Cursor object at 0x00000198DAA449D0>

>>> cursor.fetchall()

[('users',), ('items',)]


>>> users_query = """SELECT * FROM 'users';"""

>>> cursor.execute(users_query)
<sqlite3.Cursor object at 0x00000198DAA449D0>

>>>cursor.fetchall()

 [(1, 'bogdan@santa.com', 'notreallyhashed', 1), 
(2, 'basta.alpha@yahoo.com', 'o_parolanotreallyhashed', 1)]

>>> cursor.close()

>>> cursor.fetchall()

Traceback (most recent call last):
File "<input>", line 1, in <module>
sqlite3.ProgrammingError: Cannot operate on a closed cursor.
