#  Created by btrif Trif on 19-02-2023 , 8:49 PM.
import random
import string


from src.mazes.crud import get_hashed_password, verify_password, get_user_by_email, create_user, delete_user, \
    create_user_item, create_user_maze, get_mazes, get_maze_by_id, get_users, get_user_by_username

from src.mazes.schemas import UserCreateSchema, ItemCreateSchema, MazeCreateSchema
from conftest import test_current_session_local


def test_get_hashed_password() :
    test_password = "jeni"

    hashed_passwd = get_hashed_password(test_password)
    print(f"\nhashed_password : \n{hashed_passwd}            {type(hashed_passwd)}")

    assert verify_password(test_password, hashed_passwd) is True

    fake_hashed_password = get_hashed_password("1234")
    assert verify_password(test_password, fake_hashed_password) is False


def test_get_users() :
    all_users = get_users(test_current_session_local)
    for cnt, usr in enumerate(all_users) :
        print(f" {usr.id}    {usr.username}     {usr.email}  ")
    print(f"\n {type(all_users)}")
    # print(f"\n\n {type(all_users[0]) }  {all_users[0] }         ")
    assert all_users is not None


def test_get_user_by_username() :
    user_name = "alma"
    '''
    # EXAMPLE :Just make a MANUAL SESSION as model, not a real test
    test_current_session_local.query(UserModel).filter(UserModel.username == user_name).first()
    # Show the results
    for user in test_current_session_local.query(UserModel) :
        print(f"user : {user}")
    '''

    # effective test of the get_user function
    user_query_result = get_user_by_username(test_current_session_local, user_name)
    print(f"\nuser_query_result : {user_query_result}")
    print(f"\ntype user_query_result : {type(user_query_result)}")

    assert 1 == 1
    # assert isinstance(user_query_result, src.mazes.models.UserModel)




def test_get_user_by_email() :
    test_nonexisting_email = "olimpicos@realmadrid.com"
    nonexisting_email = get_user_by_email(test_current_session_local, test_nonexisting_email)

    print(f"\nnonexisting_email : \n{nonexisting_email}")

    assert nonexisting_email is None

    existing_email = "trif@trif.com"
    existing_email = get_user_by_email(test_current_session_local, existing_email)

    print(f"\nexisting_email : \n{existing_email}")


def test_create_user() :
    test_username = "biciul"
    test_email = "biciul@biciul.gov"
    test_passwd = "biciul"

    if not get_user_by_email(test_current_session_local, test_email) :
        db_test_user = UserCreateSchema(
                username=test_username,
                email=test_email,
                password=test_passwd
                )

        created_user = create_user(test_current_session_local, db_test_user)

        print(f"created_user : \n{created_user}")

        assert get_user_by_email(test_current_session_local, test_email) is not None

    assert get_user_by_email(test_current_session_local, test_email)


def test_delete_user() :
    test_username = "biciul"

    deleted_result = delete_user(test_current_session_local, test_username)
    print(f"deleted_result = \n{deleted_result}")


def generate_random_word_helper(min_nr_letters, max_nr_letters) :
    letters = [ random.choice(string.ascii_lowercase) for _ in range(random.randint(min_nr_letters, max_nr_letters)) ]
    return ''.join(letters).capitalize()


def test_create_user_item() :
    test_title = generate_random_word_helper(5, 15)
    test_description = ' '.join([ generate_random_word_helper(2, 9) for _ in range(4, 12) ])

    print(f"\ntest_title : \n{test_title}")
    print(f"\ntest_description : \n{test_description}")

    user_id = random.randint(1, 5)
    test_item = ItemCreateSchema(title=test_title, description=test_description)
    created_result = create_user_item(test_current_session_local, test_item, user_id)

    print(f"\ncreated_result : {created_result}")

    assert created_result.title is not None
    assert created_result.description is not None


def generate_random_wall_inside_maze_helper(max_row, max_col, entrance) :
    ''' Helper to generate walls inside a maze, limited by max_row and max_col
        Also, to not be an entrance '''
    while True :
        letter = string.ascii_uppercase[ random.randint(0, max_col - 1) ]
        number = str(random.randint(1, max_row))
        wall = ''.join([ letter, number ])
        if wall != entrance:
            yield wall


def test_generate_random_wall_inside_maze_helper():
    entrance = 'A1'
    wall_gen = generate_random_wall_inside_maze_helper(2,2,entrance)
    for _ in range(100):
        wall = next(wall_gen)
        print(f"wall : {wall}")
        assert wall is not None


def test_create_user_maze() :
    '''Test the creation of a random maze with walls respecting all the criteria'''
    # grid_size :  rows x cols <=> numbers x letters
    max_row, max_col = 32, 26  # max_col = from A to Z, only 26 letters
    test_row_size, test_col_size = random.randint(3, max_row), random.randint(3, max_col)
    grid_size = (f"{test_row_size}x{test_col_size}")
    print(f"\ngrid_size = {grid_size}")
    # Generate entrance
    entrance = ''.join([ string.ascii_uppercase[ random.randint(0, test_col_size - 1) ], '1' ])
    print(f"entrance : {entrance}")

    min_nr_of_walls = max_row * max_col // 9
    max_nr_of_walls = max_row * max_col // 4
    wall_gen = generate_random_wall_inside_maze_helper(test_row_size, test_col_size)
    # Generate walls
    walls = ','.join({next(wall_gen) for _ in range(min_nr_of_walls, max_nr_of_walls)})
    print(f"walls : \n{walls}")


    test_maze_configuration = MazeCreateSchema(
            grid_size=grid_size,
            walls=walls,
            entrance=entrance
            )
    print(f"\ntest_maze_configuration  : \n{test_maze_configuration}     ")

    user_id = random.randint(1, 5)
    created_maze_result = create_user_maze(test_current_session_local, test_maze_configuration, user_id)

    print(f"maze_creation_result : \n{created_maze_result}")


def test_get_mazes() :
    maze_result = get_mazes(test_current_session_local, 0, 100)
    for cnt, maze in enumerate(maze_result) :
        print(f" {maze.id}  {maze.grid_size}     {maze.owner_id}  ")
    assert maze_result is not None


def test_get_maze_by_id() :
    maze = get_maze_by_id(test_current_session_local, 1)
    print(f"maze : {maze}     , type : {type(maze)}")
    assert maze is not None
