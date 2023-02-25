#  Created by btrif Trif on 31-01-2023 , 3:56 PM.

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from src.mazes.crud import get_user_by_username, get_hashed_password, verify_password
from src.mazes.database import get_db, Base, db_engine

from src.mazes.schemas import TokenSchema

from src.mazes.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


# creates all the tables into the database; will not attempt to recreate tables already
#         present in the target database
Base.metadata.create_all(bind=db_engine)

# STARTS THE WHOLE APPLICATION
mazes_app = FastAPI()

from src.mazes.routers import users, items, mazes, admin

mazes_app.include_router(users.users_router)
mazes_app.include_router(mazes.mazes_router)
mazes_app.include_router(items.items_router)
mazes_app.include_router(admin.admin_router)


'''
###########     USERS ROUTERS       ###########


@mazes_app.post("/create_user/", response_model=UserSchema)
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


@mazes_app.get("/list_users/", response_model=list[ UserSchema ])
def read_all_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        ) :
    users = get_users(db, skip=skip, limit=limit)
    return users
    
    

@mazes_app.get("/list_users/", response_model=list[ UserSchema ])
def read_all_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        ) :
    users = get_users(db, skip=skip, limit=limit)
    return users
'''

'''
#########               ITEMS   ROUTERS    ##########


@mazes_app.post("/create_item", response_model=ItemSchema)
def create_item_for_user_only_if_authenticated(
        item: ItemCreateSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    user_id = current_user.id

    return create_user_item(db=db, item=item, user_id=user_id)



@mazes_app.get("/items", response_model=list[ ItemSchema ])
def list_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = get_items(db, skip=skip, limit=limit)
    return items


'''


@mazes_app.get("/hello")
async def simple_hello_world() :
    return {"message" : "Well Done !"}


### Second Step :    Without   token: str = Depends(oauth2_scheme)
#   the Authorization button does not appear !
#   Also, token should not be present in here !
@mazes_app.post("/token", response_model=TokenSchema)
async def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        ) :
    # 1.  Get the user from DB
    user = get_user_by_username(db, user_name=form_data.username)

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
@mazes_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

'''


# Simple redirection to /docs
@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs() :
    return RedirectResponse(url='/docs')



if __name__ == "__main__" :
    import uvicorn

    uvicorn.run("main:mazes_app", log_level="info", reload=True, port=8000)
