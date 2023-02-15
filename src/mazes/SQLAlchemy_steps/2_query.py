#  Created by btrif Trif on 15-02-2023 , 5:30 PM.

'''
Simple SELECT
With some rows in the database, here’s the simplest form of emitting a SELECT statement to load some objects.
To create SELECT statements, we use the select() function to create a new Select object,
 which we then invoke using a Session.
 The method that is often useful when querying for ORM objects is the Session.scalars() method,
 which will return a ScalarResult object that will iterate through the ORM objects we’ve selected:
'''

from sqlalchemy import select
from db_table_create_0 import User, db_engine
from sqlalchemy.orm import sessionmaker


# new session
Session = sessionmaker(bind=db_engine)
session = Session()


stmt = select(User).where(User.name.in_([ "spongebob", "sandy" ]))
print('the result:')

print('\n', '*'*30)
for user in session.scalars(stmt):
    print(f"user : {user}")

print('*' * 30, '\n')
