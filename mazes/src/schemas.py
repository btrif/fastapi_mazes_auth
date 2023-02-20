#  Created by btrif Trif on 01-02-2023 , 5:05 PM.

##########   =========       Pydantic models     =======
# https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_1_2

'''
                ===     Pydantic models ===

DOCS :  https://docs.pydantic.dev/

- Data validation and settings management using Python type annotations.

- Pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.

- Define how data should be in pure, canonical Python; validate it with pydantic.
__________________________________________________________
EXAMPLE :

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}
user = User(**external_data)
print(user.id)
#> 123
print(repr(user.signup_ts))
#> datetime.datetime(2019, 6, 1, 12, 22)
print(user.friends)
#> [1, 2, 3]
print(user.dict())
"""
{
    'id': 123,
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'friends': [1, 2, 3],
    'name': 'John Doe',
}
"""

What's going on here:

- id is of type int; the annotation-only declaration tells pydantic that this field is required. Strings,
bytes or floats will be coerced to ints if possible; otherwise an exception will be raised.

- name is inferred as a string from the provided default; because it has a default, it is not required.

- signup_ts is a datetime field which is not required (and takes the value None if it's not supplied).
pydantic will process either a unix timestamp int (e.g. 1496498400) or a string representing the date & time.

- friends uses Python's typing system, and requires a list of integers. As with id, integer-like objects will be converted to integers.


Create initial Pydantic models / schemas
Create an ItemBase and UserBase Pydantic models (or let's say "schemas") to have common attributes while creating or reading data.
And create an ItemCreate and UserCreate that inherit from them (so they will have the same attributes), 
plus any additional data (attributes) needed for creation.
So, the user will also have a password when creating it.
But for security, the password won't be in other Pydantic models, 
for example, it won't be sent from the API when reading a user.



==     Create Pydantic models / schemas for reading / returning
- Now create Pydantic models (schemas) that will be used when reading data, when returning it from the API.
- For example, before creating an item, we don't know what will be the ID assigned to it, 
but when reading it (when returning it from the API) we will already know its ID.
- The same way, when reading a user, we can now declare that items will contain the items that belong to this user.
- Not only the IDs of those items, but all the data that we defined in the Pydantic model for reading items: Item.

==     SQLAlchemy style and Pydantic style
- Notice that SQLAlchemy models define attributes using =, and pass the type as a parameter to Column, like in:

name = Column(String)

while Pydantic models declare the types using :, the new type annotation syntax/type hints:

name: str

Have it in mind, so you don't get confused when using = and : with them.



- Use Pydantic's orm_mode
- Now, in the Pydantic models for reading, Item and User, add an internal Config class.
- This Config class is used to provide configurations to Pydantic.
- In the Config class, set the attribute orm_mode = True.


== Tip:
Notice it's assigning a value with =, like:
orm_mode = True
It doesn't use : as for the type declarations before.

This is setting a config value, not declaring a type.
Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
but an ORM model (or any other arbitrary object with attributes).

This way, instead of only trying to get the id value from a dict, as in:

id = data["id"]
it will also try to get it from an attribute, as in:

id = data.id
And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the response_model argument in your path operations.

You will be able to return a database model and it will read the data from it.

= Technical Details about ORM mode
SQLAlchemy and many others are by default "lazy loading".

That means, for example, that they don't fetch the data for relationships from the database unless you try to access the attribute that would contain that data.

For example, accessing the attribute items:

current_user.items
would make SQLAlchemy go to the items table and get the items for this user, but not before.

Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data.

Even if you declared those relationships in your Pydantic models.

But with ORM mode, as Pydantic itself will try to access the data it needs from attributes (instead of assuming a dict), 
you can declare the specific data you want to return and it will be able to go and get it, even from ORMs.



################################


======   Handle JWT tokens
    Import the modules installed.

Create a random secret key that will be used to sign the JWT tokens.

To generate a secure random secret key use the command:

    #>>> openssl rand -hex 32

- And copy the output to the variable SECRET_KEY (don't use the one in the example).
- Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256".
- Create a variable for the expiration of the token.
- Define a Pydantic Model that will be used in the token endpoint for the response.
- Create a utility function to generate a new access token.


'''



from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True