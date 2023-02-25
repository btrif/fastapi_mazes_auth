#  Created by btrif Trif on 15-02-2023 , 5:29 PM.

'''
==== Create Objects and Persist

We are now ready to insert data in the database.
We accomplish this by creating instances of User and Address classes,
which have an __init__() method already as established automatically by the declarative mapping process.
We then pass them to the database using an object called a Session,
which makes use of the Engine to interact with the database.
The Session.add_all() method is used here to add multiple objects at once, and the Session.commit()
method will be used to flush any pending changes to the database and then commit the current database transaction,
which is always in progress whenever the Session is used:

from sqlalchemy.orm import Session

'''
from SQLAlchemy_steps.db_table_create_0 import *
from sqlalchemy.orm import Session, sessionmaker

# new session

Session = sessionmaker(bind=db_engine)
session = Session()

from sqlalchemy.orm import Session

# Add elements
with Session(db_engine) as session :
    # create user objects
    spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[ Address(email_address="spongebob@sqlalchemy.org") ],
            )
    sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
                ],
            )
    patrick = User(
        name="patrick",
        fullname="Patrick Star"
        )

    # Add them to the database
    session.add_all([ spongebob, sandy, patrick ])

    # Save changes into the database
    session.commit()

'''
D:\workspace\virtualenvs\fastapi_maze_jwt_auth\Scripts\python.exe D:/workspace/btrif/fastapi_mazes_auth/src/mazes/SQLAlchemy_steps/1_insert.py
2023-02-15 17:57:49,626 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 17:57:49,626 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user_account")
2023-02-15 17:57:49,626 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-02-15 17:57:49,627 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("address")
2023-02-15 17:57:49,627 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-02-15 17:57:49,627 INFO sqlalchemy.engine.Engine COMMIT
2023-02-15 17:57:49,632 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-02-15 17:57:49,633 INFO sqlalchemy.engine.Engine INSERT INTO user_account (name, fullname) VALUES (?, ?), (?, ?), (?, ?) RETURNING id
2023-02-15 17:57:49,633 INFO sqlalchemy.engine.Engine [generated in 0.00007s (insertmanyvalues)] ('spongebob', 'Spongebob Squarepants', 'sandy', 'Sandy Cheeks', 'patrick', 'Patrick Star')
2023-02-15 17:57:49,636 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?), (?, ?), (?, ?) RETURNING id
2023-02-15 17:57:49,636 INFO sqlalchemy.engine.Engine [generated in 0.00006s (insertmanyvalues)] ('spongebob@sqlalchemy.org', 1, 'sandy@sqlalchemy.org', 2, 'sandy@squirrelpower.org', 2)
2023-02-15 17:57:49,636 INFO sqlalchemy.engine.Engine COMMIT

Process finished with exit code 0


'''
