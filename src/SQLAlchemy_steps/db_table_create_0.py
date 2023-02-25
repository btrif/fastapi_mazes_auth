#  Created by btrif Trif on 15-02-2023 , 10:39 AM.

'''


https://docs.sqlalchemy.org/en/20/orm/quickstart.html

https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata

===     Declare Models

Here, we define module-level constructs that will form the structures which we will be querying from the database.
This structure, known as a Declarative Mapping, defines at once both a Python object model,
as well as database metadata that describes real SQL tables that exist, or will exist, in a particular database:


'''

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase) :
    pass


class User(Base) :
    __tablename__ = "user_account"

    id: Mapped[ int ] = mapped_column(primary_key=True)
    name: Mapped[ str ] = mapped_column(String(30))
    fullname: Mapped[ Optional[ str ] ]
    addresses: Mapped[ List[ "Address" ] ] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str :
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base) :
    __tablename__ = "address"

    id: Mapped[ int ] = mapped_column(primary_key=True)
    email_address: Mapped[ str ]
    user_id: Mapped[ int ] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[ "User" ] = relationship(back_populates="addresses")

    def __repr__(self) -> str :
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


'''
=== Create an Engine
The Engine is a factory that can create new database connections for us, 
which also holds onto connections inside of a Connection Pool for fast reuse. 
For learning purposes, we normally use a SQLite memory-only database for convenience:
'''

from sqlalchemy import create_engine
SQLITE_DATABASE = "sqlite:///../mazes_app.db"
db_engine = create_engine(SQLITE_DATABASE, echo=False)  # echo=False if you don't need messages into the console

Base.metadata.create_all(db_engine)


