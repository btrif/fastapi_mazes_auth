#  Created by btrif Trif on 19-02-2023 , 8:49 PM.
import models
from database import db_engine


from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db_engine)
session = Session()



def test_get_user():
    from crud import get_user
    user_name = "evanzo"

    # Just make a manual session as model
    session.query(models.User).filter(models.User.username == user_name).first()

    # Show the results
    for user in session.query(models.User):
        print(f"user : {user}")

    # effective test of the get_user function
    get_user_result = get_user(session, user_name )
    print(f"\nresult : {get_user_result}")

    assert get_user_result.username == user_name






