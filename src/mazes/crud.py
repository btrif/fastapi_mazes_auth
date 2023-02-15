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


'''
import models
import schemas
from utils import get_hashed_password, verify_password

'''
= Tip:

- By creating functions that are only dedicated to interacting with the database (get a user or an item) 
independent of your path operation function, you can more easily reuse them in multiple parts and also add unit tests for them.

=== Create data
Now create utility functions to create data.

== The steps are:

- Create a SQLAlchemy model instance with your data.
- add that instance object to your database session.
- commit the changes to the database (so that they are saved).
- refresh your instance (so that it contains any new data from the database, like the generated ID).

'''

from sqlalchemy.orm import Session




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> object:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # fake_hashed_password = user.password + "_notreallyhashed"
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

'''
- The SQLAlchemy model for User contains a hashed_password that should contain a secure hashed version of the password.
- But as what the API client provides is the original password, you need to extract it and generate the hashed password in your application.
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




