#  Created by btrif Trif on 01-02-2023 , 6:26 PM.


'''
=== CRUD utils
Now let's see the file sql_app/crud.py.
In this file we will have reusable functions to interact with the data in the database.

CRUD comes from: Create, Read, Update, and Delete.

...although in this example we are only creating and reading.

= Read data
- Import Session from sqlalchemy.orm, this will allow you to declare the type of
the db parameters and have better type checks and completion in your functions.

Import models (the SQLAlchemy models) and schemas (the Pydantic models / schemas).

= Create utility functions to:

- Read a single user by ID and by email.
- Read multiple users.
- Read multiple items.


= Tip:

- By creating functions that are only dedicated to interacting with the database (get a user or an item) 
independent of your path operation function, you can more easily reuse them in multiple parts and also add unit tests
for them.

=== Create data
Now create utility functions to create data.

== The steps are:

- Create a SQLAlchemy model instance with your data.
- add that instance object to your database session.
- commit the changes to the database (so that they are saved).
- refresh your instance (so that it contains any new data from the database, like the generated ID).


- The SQLAlchemy model for User contains a hashed_password that should contain a secure hashed version of the password.
- But as what the API client provides is the original password, you need to extract it and generate the hashed
password in your application.
- And then pass the hashed_password argument with the value to save.

= Warning

- This example is not secure, the password is not hashed.
- In a real life application you would need to hash the password and never save them in plaintext.
- For more details, go back to the Security section in the tutorial.
- Here we are focusing only on the tools and mechanics of databases.

=  Tip: 

- Instead of passing each of the keyword arguments to Item and reading each one of them from the Pydantic model, 
we are generating a dict with the Pydantic model's data with:

item.dict()

and then we are passing the dict's key-value pairs as the keyword arguments to the SQLAlchemy Item, with:

Item(**item.dict())

And then we pass the extra keyword argument owner_id that is not provided by the Pydantic model, with:

Item(**item.dict(), owner_id=user_id)

'''

from sqlalchemy.orm import Session

from models import User, Item, Maze
from schemas import UserCreateSchema, ItemCreateSchema, UserSchema, MazeConfigurationSchema

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=[ "bcrypt" ], deprecated="auto")


def get_hashed_password(password: str) -> str :
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool :
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_name: str) :
    return db.query(User).filter(User.username == user_name).first()


def get_user_by_email(
        db: Session,
        email: str
        ) :
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) :
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreateSchema) :
    db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_hashed_password(user.password)
            )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, email: str) :
    db_user = get_user_by_email(db, email)
    print(f"db_user from delete_user in crud : {db_user}")

    db.delete(db_user)
    db.commit()
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100) :
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemCreateSchema, user_id: int) :
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_maze(db: Session, maze_item: MazeConfigurationSchema, user_id: int) :
    print(f"create_user_maze   :   item = {maze_item}")
    db_item = Maze(
            grid_size=maze_item.grid_size,
            entrance=maze_item.entrance,
            walls=maze_item.walls,
            owner_id=user_id,

            )
    print(f"create_user_maze    :   db_item = {db_item}")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
