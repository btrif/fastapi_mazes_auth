#  Created by btrif Trif on 21-02-2023 , 6:15 PM.


from fastapi import Depends
from sqlalchemy.orm import Session

from utils import get_current_user

from crud import get_items, create_user_maze
from database import get_db

from schemas import UserSchema, ItemSchema, MazeConfigurationSchema

from fastapi import APIRouter

mazes_router = APIRouter()

mazes_router = APIRouter(
        prefix="",
        tags=[ "Mazes" ],
        # dependencies=[Depends(TokenSchema)],
        responses={404 : {"description" : "Not found"}},
        )


@mazes_router.post("/create_maze", response_model=ItemSchema)
def create_maze_for_user_only_if_authenticated(
        maze: MazeConfigurationSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    user_id = current_user.id

    return create_user_maze(
        db=db,
        maze_item=maze,
        user_id=user_id
        )


'''
@mazes_router.get("/items", response_model=list[ ItemSchema ])
def list_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = get_items(db, skip=skip, limit=limit)
    return items

'''
