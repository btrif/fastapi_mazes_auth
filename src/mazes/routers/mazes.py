#  Created by btrif Trif on 21-02-2023 , 6:15 PM.


from fastapi import Depends
from sqlalchemy.orm import Session

from src.mazes.algorithms import MazeGrid
from src.mazes.utils import get_current_user
from src.mazes.crud import create_user_maze, get_mazes, get_maze_by_id
from src.mazes.database import get_db

from src.mazes.schemas import UserSchema, MazeCreateSchema, MazeBaseSchema, MazeSchema, MazeSolution

from fastapi import APIRouter

mazes_router = APIRouter()

mazes_router = APIRouter(
        prefix="",
        tags=[ "Mazes" ],
        # dependencies=[Depends(TokenSchema)],
        responses={404 : {"description" : "Not found"}},
        )


@mazes_router.post("/create_maze", response_model=MazeSchema)
def create_maze_for_user_only_if_authenticated(
        maze: MazeCreateSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    user_id = current_user.id

    try :
        created_result = create_user_maze(
                db=db,
                maze_item=maze,
                user_id=user_id
                )
        print(f"mazes - create_maze_for_user_only_if_authenticated : {created_result}")
        return created_result

    except Exception :
        print(f'Error.   full of errors somewhere. The data was not written to DB')


@mazes_router.get("/mazes", response_model=list[ MazeSchema ])
def list_all_mazes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    db_mazes = get_mazes(db, skip=skip, limit=limit)
    return db_mazes


@mazes_router.post("/solve_maze")  # , response_model=MazeSchema)
def solve_maze(
        maze_id: int,
        db: Session = Depends(get_db), ) :
    db_maze = get_maze_by_id(db, maze_id)
    if db_maze :
        print(f"db_maze : {db_maze}     min_solution:  {db_maze.min_solution}    type : {type(db_maze)}")
        if db_maze.min_solution :
            return db_maze.min_solution

        else :
            walls = db_maze.walls
            maze_config = MazeBaseSchema(
                grid_size = db_maze.grid_size,
                entrance = db_maze.entrance,
                walls = db_maze.walls,
                )
            print(f"maze_config :   {maze_config}    {maze_config.dict()}         ")
            maze = MazeGrid(**maze_config.dict())
            maze_solution = maze.get_min_or_max_path('min')
            # return maze

        return db_maze

    return {'status' : 'error', 'message' : "this maze id does not exist"}
