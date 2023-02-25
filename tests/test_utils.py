#  Created by btrif Trif on 20-02-2023 , 4:57 PM.
from datetime import timedelta

from src.mazes.models import UserModel
from src.mazes.utils import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, create_access_token, authenticate_user

from conftest import test_current_session_local

import pytest



def test_authenticate_user():
    test_username = "alma"
    test_password = "alma"

    user_result = authenticate_user(test_current_session_local, test_username, test_password)

    print(f"\nuser_result : {user_result}")

    assert user_result is not None
    assert user_result is not False
    # assert isinstance(test_user, UserModel)
    #TODO : find a solution to fix this test when running
    # D:\workspace\btrif\fastapi_mazes_auth>python -m pytest -k authenticate tests/



def test_create_access_token():
    test_username = "hiker"
    test_password = "hiker"
    user = authenticate_user(test_current_session_local, test_username, test_password)

    print(f"\nuser : {user}")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": test_username}, expires_delta=access_token_expires
            )

    separated_token = access_token.split(".")
    print(f"\nseparated_token : \n{separated_token}")

    assert len(separated_token) == 3


def test_get_current_user():
    test_username = "arya"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    test_token = create_access_token(
            data={"sub": test_username}, expires_delta=access_token_expires
            )

    print(f"\ntest_token : \n{test_token}")

    result_cur_user = get_current_user(test_current_session_local, test_token)

    print(f"\nresult_cur_user : \n{result_cur_user}")
