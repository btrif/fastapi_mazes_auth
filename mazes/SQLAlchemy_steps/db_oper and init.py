#  Created by btrif Trif on 14-02-2023 , 2:04 PM.


from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import User, Item
from database import SQLALCHEMY_DATABASE_URL, Base

engine = create_engine(SQLALCHEMY_DATABASE_URL)

'''
with Session(engine) as session:
    # query for ``User`` objects
    statement = select(User)

    # list of ``User`` objects
    user_obj = session.scalars(statement).all()

    # query for individual columns
    statement = select(User.username, User.email)

    # list of Row objects
    rows = session.execute(statement).all()
'''

from sqlalchemy import create_engine

engine = create_engine(SQLALCHEMY_DATABASE_URL)

from sqlalchemy.orm import Session
import models


def get_user(db: Session, user_id: int) :
    return db.query(models.User).filter(models.User.id == user_id).first()


# print(f"get_user : {get_user()}")


def authenticate_user(fake_db, username: str, password: str) :
    user = get_user(fake_db, username)
    if not user :
        return False
    # if not verify_password(password, user.hashed_password) :
    #     return False
    return user


my_user = User(
        username="aretae",
        email="assdir@asd.com",
        hashed_password="asd123",
        is_active=True,
        )


def make_session_and_do() :
    with Session(engine) as sess :
        sess.begin()
        try :
            sess.add(my_user)
            print(f"my_user : {my_user.username}")
        except :
            print('here we roll back ...')
            sess.rollback()
            raise
        else :
            sess.commit()

        print(f"now we will close the session ...")
        sess.close()


#####################


from sqlalchemy.orm import sessionmaker
import sqlalchemy as db




# DEFINE THE ENGINE (CONNECTION OBJECT)
engine = db.create_engine(SQLALCHEMY_DATABASE_URL)


# CREATE THE TABLE MODEL TO USE IT FOR QUERYING
class Students(Base) :
    __tablename__ = 'students'

    first_name = db.Column(db.String(50), primary_key=True)
    last_name = db.Column(db.String(50), primary_key=True)
    course = db.Column(db.String(50), primary_key=True)
    score = db.Column(db.Float)

student1 = Students(first_name='Trif', last_name='Bogdan', course='Python', score=9.95)

# CREATE A SESSION OBJECT TO INITIATE QUERY
# IN DATABASE
Session = sessionmaker(bind=engine)
session = Session()



session.add(student1)
session.commit()
