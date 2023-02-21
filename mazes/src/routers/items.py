#  Created by btrif Trif on 21-02-2023 , 6:15 PM.


from fastapi import Depends
from sqlalchemy.orm import Session

from utils import get_current_user

from crud import create_user_item, get_items
from database import get_db

from schemas import UserSchema, ItemCreateSchema, ItemSchema

from fastapi import APIRouter
items_router = APIRouter()

items_router = APIRouter(
        prefix="",
        tags=["Items"],
        # dependencies=[Depends(TokenSchema)],
        responses={404: {"description": "Not found"}},
        )



@items_router.post("/create_item", response_model=ItemSchema)
def create_item_for_user_only_if_authenticated(
        item: ItemCreateSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    user_id = current_user.id

    return create_user_item(db=db, item=item, user_id=user_id)



@items_router.get("/items", response_model=list[ ItemSchema ])
def list_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = get_items(db, skip=skip, limit=limit)
    return items

