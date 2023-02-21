#  Created by btrif Trif on 19-02-2023 , 8:49 PM.
import models
from database import db_engine


from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

this_session = sessionmaker(bind=db_engine)
current_test_session = this_session()



def test_get_user():
    from crud import get_user
    user_name = "evanzo"

    # Just make a manual session as model, not a real test
    current_test_session.query(models.User).filter(models.User.username == user_name).first()

    # Show the results
    for user in current_test_session.query(models.User):
        print(f"user : {user}")

    # effective test of the get_user function
    get_user_result = get_user(current_test_session, user_name)
    print(f"\nresult : {get_user_result}")

    assert get_user_result.username == user_name






