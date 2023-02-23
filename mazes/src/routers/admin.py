#  Created by btrif Trif on 21-02-2023 , 6:02 PM.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import delete_user
from database import get_db
from schemas import TokenSchema, UserBaseSchema, UserSchema
from utils import get_current_user

admin_router = APIRouter(
        prefix="",
        tags=[ "admin" ],
        dependencies=[ Depends(TokenSchema) ],
        responses={
            404 : {"description" : "Not found"},
            418 : {"description" : "I'm a teapot"},
            },
        )


@admin_router.post("/admin")
async def update_admin() :
    return {"message" : "Admin getting schwifty"}


@admin_router.post("/delete_user", response_model=UserBaseSchema)
async def delete_username(
        user: UserBaseSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    deleted_user = delete_user(
            db=db,
            username=user.username
            )
    #TODO To fix this
    return deleted_user
