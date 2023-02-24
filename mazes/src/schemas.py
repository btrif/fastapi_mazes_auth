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

- friends uses Python's typing system, and requires a list of integers. As with id, integer-like objects will be
converted to integers.


Create initial Pydantic models / schemas
Create an ItemBase and UserBase Pydantic models (or let's say "schemas") to have common attributes while creating or
reading data.
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
And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the response_model argument
in your path operations.

You will be able to return a database model and it will read the data from it.

= Technical Details about ORM mode
SQLAlchemy and many others are by default "lazy loading".

That means, for example, that they don't fetch the data for relationships from the database unless you try to access
the attribute that would contain that data.

For example, accessing the attribute items:

current_user.items
would make SQLAlchemy go to the items table and get the items for this user, but not before.

Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship
data.

Even if you declared those relationships in your Pydantic models.

But with ORM mode, as Pydantic itself will try to access the data it needs from attributes (instead of assuming a
dict),
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
import string
import re

from typing import Union, List

from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, validator, ValidationError, root_validator


###########         Item Schema        ############

class ItemBaseSchema(BaseModel) :
    title: str
    description: Union[ str, None ] = None


class ItemCreateSchema(ItemBaseSchema) :
    pass


class ItemSchema(ItemBaseSchema) :
    id: int
    owner_id: int

    class Config :
        orm_mode = True


###########         Maze Schemas        ############
'''
We will use validators to check our schemas
https://docs.pydantic.dev/usage/validators/
'''


class MazeBaseSchema(BaseModel) :
    grid_size: str
    walls: str
    entrance: str


class MazeSchema(MazeBaseSchema) :
    id: int
    owner_id: int

    class Config :
        orm_mode = True


class MazeCreateSchema(MazeBaseSchema) :

    @validator('grid_size')
    def validate_grid(cls, grid_size) :
        ''' method to validate grid'''
        # 33x26
        import re
        grid_pattern = re.compile("^[0-9]{1,2}x[0-9]{1,2}$")  # 10x13
        match_grid = re.match(grid_pattern, grid_size)
        print(f"validate_grid  match_grid : {match_grid}")
        if not match_grid :
            raise HTTPException(f"ValidationError : grid_size must be of the form : 32x26 and no spaces. Example : 9x12")

        assert match_grid, f"ValidationError : grid_size must be of the form : 32x26 and no spaces. Example : 9x12"

        return grid_size


    @validator('grid_size')
    def check_grid_size(cls, grid_size) :
        ''' Grid size limitation'''
        rows, cols = map(int, grid_size.split('x'))
        print(f"grid_size :  rows, cols   {rows, cols}")

        assert (rows <= 32 or cols <= 26), f"ValidationError : grid_size values max rows = 32 and max cols = 26"

        if (rows > 32 or cols > 26) :
            raise HTTPException(f"ValidationError : grid_size values max rows = 32 and max cols = 26")

        return grid_size


    @validator('walls')
    def check_at_least_one_wall(cls, walls) :

        # first group    [A-Z]\d{1,2}   matches only :  C99
        # second group    (,[A-Z]\d{1,2})*    is greedy and matches:     ,A2,B13,E7,D2,B5      . That is why they are separated
        walls_pattern = "^[A-Z]\d{1,2}(,[A-Z]\d{1,2})*$"
        match_walls = re.match(walls_pattern, walls)
        print(f"validate_grid  match_walls : {match_walls}")
        # if not match_walls :
        #     raise HTTPException(f"ValidationError : Walls must have no spaces and must be separated by comma. A
        #     valid group looks like : "
        #                         f"C4,A2,B13,E7,D2,B5 . Please check carefully your walls ")

        assert match_walls, f"ValidationError : walls must have no spaces and must be separated by comma. A valid " \
                            f"group looks like : " \
                            f"C4,A2,B13,E7,D2,B5 . Please check carefully your walls "

        return walls


    @root_validator
    def check_walls_are_within_grid_size(cls, walls_in_grid) :
        '''     Concrete example :
            - If we define  a grid of 4x4 where we have elements from A, B, C, D --> 1, 2, 3, 4:
                - we must have elements from A1 to D4
                - we cannot have elements like A5, E2, B6, ...
         '''

        walls = walls_in_grid.get('walls')
        grid_size = walls_in_grid.get('grid_size')
        entrance = walls_in_grid.get('entrance')
        print(f'walls_list :  {walls}   {type(walls)}')
        print(f'grid_size :  {grid_size}   {type(grid_size)}')
        assert walls, f"Invalid walls from check_walls_are_within_grid_size"
        assert grid_size, f"grid_size has not the proper dimensions"

        rows_size, cols_size = map(int, grid_size.split('x'))
        print(f"rows, cols = {rows_size}  {cols_size}")

        col_letters = set(string.ascii_uppercase[ :cols_size ])
        print(f"cols_letters : {sorted(col_letters)}")

        ### Check columns ( which are letters )
        walls_letters = {letter[ :1 ] for letter in walls.split(',')}
        assert len(
            walls_letters - col_letters
            ) == 0, f"{walls_letters - col_letters} within walls Column letters are not allowed"
        print(f"walls_letters :  {walls_letters}")

        # Check rows (which are numbers )
        walls_numbers = {int(nr[ 1 : ]) for nr in walls.split(',')}
        print(f"walls_numbers : {walls_numbers}")
        assert max(
            walls_numbers
            ) <= rows_size, f"{walls_numbers - set(range(1, rows_size + 1))} within walls row numbers are too big. Maximum possible nr is {rows_size}. "


        ###    Check entrance(cls, entrance) :
        '''
        - We want to make sure that we always have an entrance in the TOP ROW
        - Valid entrance should be only one letter [A-Z] followed by digit 1 : A1, T1, Z1.
        - Invalid entrances : A2, Z8, AB1, XY1,
        '''
        col_entrance, row_entrance = entrance[ :1 ], entrance[ 1 : ]
        assert col_entrance in string.ascii_uppercase, f"entrance's first character must be an uppercase letter "
        assert  row_entrance == '1', f"entrance's second character must be a always the digit 1. Represents the top row of the maze. "

        # Check letter_entrance is valid. You cannot have S in a column size = 5 with letters [A,B,C,D,E]
        assert col_entrance in col_letters, f"entrance\'s letter \'{col_entrance}\' does not fit within column size of {cols_size}. " \
                                            f"Last valid letter must be \'{string.ascii_uppercase[rows_size]}\'. "


        return walls_in_grid





###########         User Schema        ############

class UserBaseSchema(BaseModel) :
    username: str


class UserCreateSchema(UserBaseSchema) :
    email: str
    password: str


class UserSchema(UserBaseSchema) :
    id: int
    is_active: bool
    mazes: list[ MazeSchema ] = [ ]
    items: list[ ItemSchema ] = [ ]

    class Config :
        orm_mode = True


###########         Token Schema        ############

class TokenSchema(BaseModel) :
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel) :
    username: Union[ str, None ] = None


###### First condition required for Token Authorize button           #######
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

if __name__ == '__main__' :
    maze_config = MazeCreateSchema(
            grid_size=" 9 x -   11",
            walls='B2, C3, A4, A5, B6, B13, C14, E1, F7, A14',
            entrance='AC1 B3'
            )
    print(f"maze_config  : {maze_config}     ")
    print(f"walls type  : {type(maze_config.walls)}     ")
