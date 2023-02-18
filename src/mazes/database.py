#  Created by btrif Trif on 01-02-2023 , 10:59 AM.
# https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_1_2

'''
=== Create a database URL for SQLAlchemy

- In this example, we are "connecting" to a SQLite database (opening a file with the SQLite database).
- The file will be located at the same directory in the file sql_app.db.
- That's why the last part is ./sql_app.db.

- If you were using a PostgreSQL database instead, you would just have to uncomment the line:

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
...and adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other).

- Tip :
This is the main line that you would have to modify if you wanted to use a different database.

- If you were using a PostgreSQL database instead, you would just have to uncomment the line:
- SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
...and adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other).


sqlalchemy.exc.ArgumentError: Invalid SQLite URL: sqlite://mazes_app.db
Valid SQLite URL forms are:
sqlite:///:memory: (or, sqlite://)
sqlite:///relative/path/to/file.db
sqlite:////absolute/path/to/file.db


== Create the SQLAlchemy engine
- The first step is to create a SQLAlchemy "engine".
- We will later use this engine in other places.

Note:
The argument:
connect_args={"check_same_thread": False}
...is needed only for SQLite. It's not needed for other databases.

==  Technical Details

- By default SQLite will only allow one thread to communicate with it, 
assuming that each thread would handle an independent request.
- This is to prevent accidentally sharing the same connection for different things (for different requests).
- But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same
request,
so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
- Also, we will make sure each request gets its own database connection session in a dependency, 
so there's no need for that default mechanism.


== Create a SessionLocal class
- Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
- But once we create an instance of the SessionLocal class, this instance will be the actual database session.
- We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
- We will use Session (the one imported from SQLAlchemy) later.
- To create the SessionLocal class, use the function sessionmaker:



== Create a Base class
- Now we will use the function declarative_base() that returns a class.
- Later we will inherit from this class to create each of the database models or classes (the ORM models):
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///mazes_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

db_engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()
