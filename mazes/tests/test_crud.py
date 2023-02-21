#  Created by btrif Trif on 19-02-2023 , 8:49 PM.
import random
import string

import models
from crud import get_hashed_password, verify_password, get_user_by_email, create_user, delete_user, create_user_item
from database import db_engine

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from schemas import UserCreateSchema, ItemCreateSchema

this_session = sessionmaker(bind=db_engine)
current_test_session = this_session()


def test_get_hashed_password() :
    test_password = "jeni"

    hashed_passwd = get_hashed_password(test_password)
    print(f"\nhashed_password : \n{hashed_passwd}            {type(hashed_passwd)}")

    assert verify_password(test_password, hashed_passwd) is True

    fake_hashed_password = get_hashed_password("1234")
    assert verify_password(test_password, fake_hashed_password) is False


def test_get_user() :
    from crud import get_user
    user_name = "evanzo"

    # Just make a manual session as model, not a real test
    current_test_session.query(models.User).filter(models.User.username == user_name).first()

    # Show the results
    for user in current_test_session.query(models.User) :
        print(f"user : {user}")

    # effective test of the get_user function
    get_user_result = get_user(current_test_session, user_name)
    print(f"\nresult : {get_user_result}")

    assert get_user_result.username == user_name


def test_get_user_by_email() :
    test_nonexisting_email = "olimpicos@realmadrid.com"
    nonexisting_email = get_user_by_email(current_test_session, test_nonexisting_email)

    print(f"\nnonexisting_email : \n{nonexisting_email}")

    assert nonexisting_email is None

    existing_email = "trif@trif.com"
    existing_email = get_user_by_email(current_test_session, existing_email)

    print(f"\nexisting_email : \n{existing_email}")


def test_create_user() :
    test_username = "biciul"
    test_email = "biciul@biciul.eu"
    test_passwd = "biciul"

    if not get_user_by_email(current_test_session, test_email) :
        db_test_user = UserCreateSchema(
                username=test_username,
                email=test_email,
                password=test_passwd
                )

        created_user = create_user(current_test_session, db_test_user)

        print(f"created_user : \n{created_user}")

        assert get_user_by_email(current_test_session, test_email) is not None

    assert get_user_by_email(current_test_session, test_email)


def test_delete_user() :
    test_email = "biciul@biciul.eu"

    deleted_result = delete_user(current_test_session, test_email)
    print(f"deleted_result = \n{deleted_result}")


def generate_random_word_helper(min_nr_letters, max_nr_letters) :
    letters = [ random.choice(string.ascii_lowercase) for _ in range(random.randint(min_nr_letters, max_nr_letters)) ]
    return ''.join(letters).capitalize()


def test_create_user_item() :
    test_title = generate_random_word_helper(5, 15)
    test_description = ' '.join([ generate_random_word_helper(2, 9) for _ in range(4, 12) ])

    print(f"\ntest_title : \n{test_title}")
    print(f"\ntest_description : \n{test_description}")

    user_id = random.randint(1, 7)
    test_item = ItemCreateSchema(title=test_title, description=test_description)
    created_result = create_user_item(current_test_session, test_item, user_id)

    print(f"\ncreated_result : {created_result}")

    assert created_result.title is not None
    assert created_result.description is not None
