#  Created by btrif Trif on 31-01-2023 , 5:11 PM.

##########   =========       SQLAlchemy models     =======

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String



from sqlalchemy.orm import relationship

from database import Base

'''
=== Create the database models
- Let's now see the file sql_app/models.py.

== Create SQLAlchemy models from the Base class¶
- We will use this Base class we created before to create the SQLAlchemy models.

- Tip:
- SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
- But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.


- Import Base from database (the file database.py from above).
- Create classes that inherit from it.
- These classes are the SQLAlchemy models.
- The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
'''

'''
=== Create model attributes/columns
- Now create all the model (class) attributes.
- Each of these attributes represents a column in its corresponding database table.
- We use Column from SQLAlchemy as the default value.
- And we pass a SQLAlchemy class "type", as Integer, String, and Boolean, that defines the type in the database, as an argument.

'''




'''
== Create the relationships
- Now create the relationships.
- For this, we use relationship provided by SQLAlchemy ORM.
- This will become, more or less, a "magic" attribute that will contain the values from other tables related to this one.
items = relationship("Item", back_populates="owner")

- When accessing the attribute items in a User, as in my_user.items, 
it will have a list of Item SQLAlchemy models (from the items table) 
that have a foreign key pointing to this record in the users table.
- When you access my_user.items, SQLAlchemy will actually go and fetch the items 
from the database in the items table and populate them here.
- And when accessing the attribute owner in an Item, it will contain a User SQLAlchemy model from the users table. 
It will use the owner_id attribute/column with its foreign key to know which record to get from the users table.

'''

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")