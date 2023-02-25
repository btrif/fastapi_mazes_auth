#  Created by btrif Trif on 15-02-2023 , 9:34 PM.

'''
===Make Changes

The Session object, in conjunction with our ORM-mapped classes User and Address,
automatically track changes to the objects as they are made,
which result in SQL statements that will be emitted the next time the Session flushes.
Below, we change one email address associated with “sandy”, and also add a new email address to “patrick”,
after emitting a SELECT to retrieve the row for “patrick”:

'''


from sqlalchemy import select
from db_table_create_0 import User, Address, db_engine
from sqlalchemy.orm import sessionmaker


# new session
Session = sessionmaker(bind=db_engine)
session = Session()


# Select
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
print(f"\npatrick : {patrick}")

patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))


# ########           SELECT with JOIN and Make Changes  #####################
print("\n","*"*15, "    SELECT with JOIN and Make Changes    ", "*"*15)

stmt2 = (
    select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
)

# # Using Scalars
sandy_address = session.scalars(stmt2).one()

print(f"\nsandy_address : {sandy_address}")
sandy_address.email_address = "sandy_cheeks_bogdan@sqlalchemy.org"


# Write the changes to the DB
session.commit()


'''
CONSOLE RESULTS :

D:\workspace\virtualenvs\fastapi_maze_jwt_auth\Scripts\python.exe D:/workspace/btrif/fastapi_mazes_auth/src/mazes/SQLAlchemy_steps/3_update_delete.py
2023-02-15 21:52:09,883 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 21:52:09,884 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user_account")
2023-02-15 21:52:09,884 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-02-15 21:52:09,884 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("address")
2023-02-15 21:52:09,884 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-02-15 21:52:09,884 INFO sqlalchemy.engine.Engine COMMIT
2023-02-15 21:52:09,885 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 21:52:09,889 INFO sqlalchemy.engine.Engine SELECT user_account.id, user_account.name, user_account.fullname 
FROM user_account 
WHERE user_account.name = ?
2023-02-15 21:52:09,889 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ('patrick',)

patrick : User(id=3, name='patrick', fullname='Patrick Star')
2023-02-15 21:52:09,891 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id 
FROM address 
WHERE ? = address.user_id
2023-02-15 21:52:09,891 INFO sqlalchemy.engine.Engine [generated in 0.00010s] (3,)
2023-02-15 21:52:09,893 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?)
2023-02-15 21:52:09,893 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ('patrickstar@sqlalchemy.org', 3)
2023-02-15 21:52:09,905 INFO sqlalchemy.engine.Engine SELECT address.id, address.email_address, address.user_id 
FROM address JOIN user_account ON user_account.id = address.user_id 
WHERE user_account.name = ? AND address.email_address = ?
2023-02-15 21:52:09,905 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ('sandy', 'sandy@sqlalchemy.org')

sandy_address : Address(id=2, email_address='sandy@sqlalchemy.org')
2023-02-15 21:52:09,906 INFO sqlalchemy.engine.Engine UPDATE address SET email_address=? WHERE address.id = ?
2023-02-15 21:52:09,906 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ('sandy_cheeks_bogdan@sqlalchemy.org', 2)
2023-02-15 21:52:09,906 INFO sqlalchemy.engine.Engine COMMIT

Process finished with exit code 0

'''

#####################################

print('\n','*'*15, '        SOME DELETES               ' , '*'*15 )

'''
    === Some Deletes
    
All things must come to an end, as is the case for some of our database rows - here’s a quick demonstration 
of two different forms of deletion, both of which are important based on the specific use case.

First we will remove one of the Address objects from the “sandy” user. 
When the Session next flushes, this will result in the row being deleted. 
This behavior is something that we configured in our mapping called the delete cascade. 
We can get a handle to the sandy object by primary key using Session.get(), then work with the object:

'''

sandy = session.get(User, 2)
print(f"\nsandy again : {sandy}")

sandy.addresses.remove(sandy_address)

'''
The last SELECT above was the lazy load operation proceeding so that the sandy.addresses collection could be loaded, 
so that we could remove the sandy_address member. 
There are other ways to go about this series of operations that won’t emit as much SQL.

We can choose to emit the DELETE SQL for what’s set to be changed so far, 
without committing the transaction, using the Session.flush() method:
'''

session.flush()

'''
Next, we will delete the “patrick” user entirely. 
For a top-level delete of an object by itself, we use the Session.delete() method; 
this method doesn’t actually perform the deletion, but sets up the object to be deleted on the next flush. 
The operation will also cascade to related objects based on the cascade options that we configured, in this case, onto the related Address objects:

'''
session.commit()

'''

The Session.delete() method in this particular case emitted two SELECT statements, 
even though it didn’t emit a DELETE, which might seem surprising. 
This is because when the method went to inspect the object, it turns out the patrick object was expired, 
which happened when we last called upon Session.commit(), 
and the SQL emitted was to re-load the rows from the new transaction. 
This expiration is optional, and in normal use we will often be turning it off for situations where it doesn’t apply well.

To illustrate the rows being deleted, here’s the commit:
'''

session.delete(patrick)

'''
2023-02-15 22:03:40,681 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 22:03:40,681 INFO sqlalchemy.engine.Engine SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname 
FROM user_account 
WHERE user_account.id = ?
2023-02-15 22:03:40,681 INFO sqlalchemy.engine.Engine [generated in 0.00010s] (2,)

sandy again : User(id=2, name='sandy', fullname='Sandy Cheeks')
2023-02-15 22:03:40,682 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id 
FROM address 
WHERE ? = address.user_id
2023-02-15 22:03:40,682 INFO sqlalchemy.engine.Engine [cached since 0.02381s ago] (2,)
2023-02-15 22:03:40,683 INFO sqlalchemy.engine.Engine DELETE FROM address WHERE address.id = ?
2023-02-15 22:03:40,683 INFO sqlalchemy.engine.Engine [generated in 0.00009s] (2,)
2023-02-15 22:03:40,683 INFO sqlalchemy.engine.Engine COMMIT
2023-02-15 22:03:40,685 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 22:03:40,686 INFO sqlalchemy.engine.Engine SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname 
FROM user_account 
WHERE user_account.id = ?
2023-02-15 22:03:40,686 INFO sqlalchemy.engine.Engine [generated in 0.00011s] (3,)
2023-02-15 22:03:40,686 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id 
FROM address 
WHERE ? = address.user_id
2023-02-15 22:03:40,687 INFO sqlalchemy.engine.Engine [cached since 0.0286s ago] (3,)

Process finished with exit code 0


'''