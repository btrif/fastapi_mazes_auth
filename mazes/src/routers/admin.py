#  Created by btrif Trif on 21-02-2023 , 6:02 PM.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import delete_user, get_user_by_username
from database import get_db

from schemas import UserBaseSchema, UserSchema
from utils import get_current_user

admin_router = APIRouter(
        prefix="",
        tags=[ "admin" ],
        # dependencies=[ Depends(TokenSchema) ],
        responses={
            404 : {"description" : "Not found"},
            },
        )


@admin_router.post("/admin")
async def update_admin() :
    return {"message" : "Admin getting schwifty"}



@admin_router.post("/delete_user", response_model=dict)
async def delete_username(
        user: UserBaseSchema,
        current_user: UserBaseSchema = Depends(get_current_user),
        db: Session = Depends(get_db),
        ) :
    loggedin_user = current_user.username
    print(f"loggedin_user : {loggedin_user}   {type(loggedin_user)}   ")

    if loggedin_user in {'admin'} :
        db_user = get_user_by_username(
                db,
                user_name=user.username
                )
        if db_user :
            print(f"delete_user_by_username db_user :  {db_user}")
            deleted_user = delete_user(
                    db=db,
                    user_name=user.username
                    )
            print(f"deleted_user : {deleted_user}")
        else :
            raise HTTPException(status_code=400, detail="This username does not exist")

        return {"status" : "ok", "message" : f"The user {user.username} was successfully deleted"}

    else :
        raise HTTPException(status_code=400, detail="Only administrators can delete accounts")
