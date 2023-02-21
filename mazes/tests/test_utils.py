#  Created by btrif Trif on 20-02-2023 , 4:57 PM.
from datetime import timedelta



from utils import get_hashed_password, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user


def test_get_hashed_password():
    test_password = "jeni"

    hashed_passwd = get_hashed_password(test_password)
    print(f"\nhashed_password : \n{hashed_passwd}            {type(hashed_passwd)}")

    assert verify_password(test_password, hashed_passwd) is True

    fake_hashed_password = get_hashed_password("1234")
    assert verify_password(test_password, fake_hashed_password ) is False




from utils import authenticate_user
from database import db_engine
from sqlalchemy.orm import sessionmaker

SessionLocalTest = sessionmaker(bind=db_engine)
test_session = SessionLocalTest()


def test_authenticate_user():
    test_username = "hiker"
    test_password = "hiker"

    test_user = authenticate_user(test_session, test_username, test_password)

    print(f"test_user : {test_user}")

    assert test_user is not False


from utils import create_access_token

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
