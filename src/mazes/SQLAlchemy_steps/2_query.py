#  Created by btrif Trif on 15-02-2023 , 5:30 PM.

'''
==== Simple SELECT


With some rows in the database, here’s the simplest form of emitting a SELECT statement to load some objects.
To create SELECT statements, we use the select() function to create a new Select object,
 which we then invoke using a Session.
 The method that is often useful when querying for ORM objects is the Session.scalars() method,
 which will return a ScalarResult object that will iterate through the ORM objects we’ve selected:
'''

from sqlalchemy import select
from db_table_create_0 import User, Address, db_engine
from sqlalchemy.orm import sessionmaker


# new session
Session = sessionmaker(bind=db_engine)
session = Session()


simple_stmt = select(User).where(User.name.in_([ "spongebob", "sandy" ]))
print('*'*15, "   Simple SELECT with Scalars   " , '*'*15)


for user in session.scalars(simple_stmt):
    print(f"user : {user}")

##################  Simple SELECT with query ######################

print('*' * 30, '\n')
print('*'*15, "   Simple SELECT with query   " , '*'*15)

for user in session.query(User):
    print(f"user : {user}")


print('*' * 30, '\n')



print('*'*15, "SELECT with JOIN" , '*'*15)

# JOIN Statement
join_stmt = (
    select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(join_stmt).one()
print(f"\nsandy_address : {sandy_address}")

print('*' * 30, '\n')