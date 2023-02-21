#  Created by btrif Trif on 31-01-2023 , 3:56 PM.
import subprocess
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from crud import get_user, get_user_by_email, get_hashed_password, verify_password, create_user_item
from database import get_db

from schemas import oauth2_scheme, UserSchema, TokenSchema, UserCreateSchema, ItemCreateSchema, ItemSchema

from utils import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

mazes_app = FastAPI()

'''mazes_app.include_router(routers.docs)
mazes_app.include_router(

        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(fake_decode_token)],
        responses={418: {"description": "I'm a teapot"}},
        )
'''


@mazes_app.post("/create_user/", response_model=UserSchema)
def create_user(
        user: UserCreateSchema,
        db: Session = Depends(get_db)
        ) :

    db_user = get_user_by_email(
            db,
            email=user.email
            )

    if db_user :
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(
            db=db,
            user=user
            )


'''
@mazes_app.get("/users/", response_model=list[ schemas.User ])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),

        ) :
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
'''


@mazes_app.post("/users/{user_id}/items/", response_model=ItemSchema)
def create_item_for_user_only_if_authenticated(
        user_id: int,
        item: ItemCreateSchema,
        db: Session = Depends(get_db)
        ) :
    return create_user_item(db=db, item=item, user_id=user_id)




@mazes_app.get("/hello")
async def simple_hello_world() :
    return {"message" : "Well Done !"}



@mazes_app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)) :
    return current_user


@mazes_app.get("/my_user", response_model=dict)
async def hello_user(current_user: UserSchema = Depends(get_current_user)) :

    date = datetime.now().strftime("%d.%m.%Y")
    time = datetime.now().strftime("%H:%M")
    processor = str(subprocess.check_output([ "wmic", "cpu", "get", "name" ]).strip()).split('\\n')[ 1 ]

    return {
        "message" : {
            "Your username is : " : current_user.username,
            "Today is" : date,
            "Time is" : time,
            "processor" : processor,
            "and you have the following items : " : current_user.items,

            }
        }




### Second Step :    Without   token: str = Depends(oauth2_scheme)
#   the Authorization button does not appear !
#   Also, token should not be present in here !
@mazes_app.post("/token", response_model=TokenSchema)
async def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        ) :
    # 1.  Get the user from DB
    user = get_user(db, user_name=form_data.username)

    if user is None :
        raise HTTPException(
                status_code=404, detail="User not found",
                headers={"WWW-Authenticate" : "Bearer"},
                )
    print(f"form_data typed user : {form_data.username}")
    print(f" form_data  'typed passwd: ' {form_data.password}")
    print(f"hashed_password : {get_hashed_password(form_data.password)}")
    print(f"password from DB : {user.hashed_password}")

    # 2. Check password :
    user_hashed_passwd = user.hashed_password
    print(f"Check : {verify_password(form_data.password, user.hashed_password)}")

    if not verify_password(form_data.password, user.hashed_password) :
        raise HTTPException(
                status_code=400,
                detail="Incorrect password",
                headers={"WWW-Authenticate" : "Bearer"},
                )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub" : user.username}, expires_delta=access_token_expires
            )
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
        }




'''
@mazes_app.get("/items/", response_model=list[ schemas.Item ])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
'''


# Simple redirection to /docs
@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs() :
    return RedirectResponse(url='/docs')


if __name__ == "__main__" :
    import uvicorn

    uvicorn.run("main:mazes_app", log_level="info", reload=True, port=8000)
