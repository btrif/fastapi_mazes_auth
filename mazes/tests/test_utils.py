#  Created by btrif Trif on 20-02-2023 , 4:57 PM.
from datetime import timedelta

from utils import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, create_access_token, authenticate_user

from database import db_engine
from sqlalchemy.orm import sessionmaker

# Make local session
SessionLocalTest = sessionmaker(bind=db_engine)
test_session = SessionLocalTest()


def test_authenticate_user():
    test_username = "hiker"
    test_password = "hiker"

    test_user = authenticate_user(test_session, test_username, test_password)

    print(f"test_user : {test_user}")

    assert test_user is not False




def test_create_access_token():
    test_username = "hiker"
    test_password = "hiker"
    user = authenticate_user(test_session, test_username, test_password)

    print(f"\nuser : {user}")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": test_username}, expires_delta=access_token_expires
            )

    separated_token = access_token.split(".")
    print(f"\nseparated_token : \n{separated_token}")

    assert len(separated_token) == 3


def test_get_current_user():
    test_username = "hiker"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    test_token = create_access_token(
            data={"sub": test_username}, expires_delta=access_token_expires
            )

    print(f"\ntest_token : \n{test_token}")

    result_cur_user = get_current_user(test_session, test_token)

    print(f"\nresult_cur_user : \n{result_cur_user}")