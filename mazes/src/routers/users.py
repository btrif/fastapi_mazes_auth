#  Created by btrif Trif on 21-02-2023 , 5:51 PM.
from datetime import timedelta, datetime
import subprocess

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from utils import get_current_user

from crud import get_user_by_email, get_users, create_user
from database import get_db

from schemas import UserSchema, TokenSchema, UserCreateSchema

from fastapi import APIRouter
users_router = APIRouter()

users_router = APIRouter(
        prefix="",
        tags=["Users"],
        # dependencies=[Depends(TokenSchema)],
        responses={404: {"description": "Not found"}},
        )


@users_router.post("/create_user/", response_model=UserSchema)
def create_new_user(
        user: UserCreateSchema,
        db: Session = Depends(get_db)
        ) :

    db_user = get_user_by_email(
            db,
            email=user.email
            )

    print(f"create_user db_user :  {db_user}")

    if db_user :
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(
            db=db,
            user=user
            )


@users_router.get("/list_users/", response_model=list[ UserSchema ])
def read_all_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        ) :
    users = get_users(db, skip=skip, limit=limit)
    return users



@users_router.get("/read_myself", response_model=UserSchema)
async def read_my_user_only_if_authenticated(current_user: UserSchema = Depends(get_current_user)) :
    return current_user


@users_router.get("/hello_myself", response_model=dict)
async def hello_my_user_only_if_authenticated(current_user: UserSchema = Depends(get_current_user)) :
    date = datetime.now().strftime("%d.%m.%Y")
    time = datetime.now().strftime("%H:%M")
    processor = str(subprocess.check_output([ "wmic", "cpu", "get", "name" ]).strip()).split('\\n')[ 1 ]

    return {
        "message" : {
            "Your username is : " : current_user.username,
            "Today is" : date,
            "Time is" : time,
            "processor" : processor,
            "and you have the following mazes : " : current_user.mazes,
            }
        }



