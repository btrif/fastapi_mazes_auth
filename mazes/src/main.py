#  Created by btrif Trif on 31-01-2023 , 3:56 PM.

from fastapi.responses import RedirectResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
from schemas import User
import models
from database import SessionLocal, db_engine


# creates all the tables into the database; will not attempt to recreate tables already
#         present in the target database
models.Base.metadata.create_all(bind=db_engine)

mazes_app = FastAPI()

# First condition required for Token Authorize button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


'''
@mazes_app.post("/create_user/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
        ) :
    db_user = crud.get_user_by_email(
            db,
            email=user.email
            )
    if db_user :
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(
            db=db,
            user=user
            )

'''

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

'''
@mazes_app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int,
        item: schemas.ItemCreate,
        db: Session = Depends(get_db)
        ) :
    return crud.create_user_item(db=db, item=item, user_id=user_id)

'''

'''
@mazes_app.get("/hello")
async def simple_hello_world() :
    # return {"message": "Hello World"}

    date = datetime.now().strftime("%d.%m.%Y")
    time = datetime.now().strftime("%H:%M")
    processor = str(subprocess.check_output([ "wmic", "cpu", "get", "name" ]).strip()).split('\\n')[ 1 ]

    return {
        "message" : {
            "Hello" : "World",
            "Today is" : date,
            "and the time is" : time,
            "processor" : processor
            }
        }

'''


def fake_decode_token( token) :
    # This doesn't provide any security at all
    # Check the next version
    user = crud.get_user(get_db, token)
    return user


# Method required for Authorization Button
# token: str = Depends(oauth2_scheme)   is REQUIRED
async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
        ) :

    operation1 = fake_decode_token( token)
    print(f"operation1 : {operation1}")

    username = crud.get_user(db, user_name=token)
    print(f"token is : {token}")
    print(f"username is : {username}")

    if not username :
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate" : "Bearer"},
                )
    return username


# Third Required Step for Authorization Button
@mazes_app.get("/user")
async def read_user(
        username: User = Depends(get_current_user),
        ) :



    return username


# Second Step :    Without   token: str = Depends(oauth2_scheme)
# the Authorization button does not appear !
# Also, token should not be present in here !
@mazes_app.post("/token")
async def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        ) :
    # 1.  Get the user from DB
    user = crud.get_user(db, user_name=form_data.username)

    if user is None :
        raise HTTPException(status_code=404, detail="User not found")
    print(f"form_data typed user : {form_data.username}   'typed passwd: ' {form_data.password}")

    # 2. Check password :
    user_passwd = form_data.password
    if not user_passwd == user.hashed_password :
        raise HTTPException(status_code=400, detail="Incorrect password")

    return user


'''
@mazes_app.get("/hello_user")
async def hello_user(
        username: str,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
        form_data: OAuth2PasswordRequestForm = Depends()
        ) :
    db_user = crud.get_user(db, user_name=username)
    if db_user is None :
        raise HTTPException(status_code=404, detail="User not found")



    return {
        "message" : {
            "Hello" : db_user,
            # "form_data.username" : form_data.username,
            }
        }
'''


# Simple redirection to /docs
@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs() :
    return RedirectResponse(url='/docs')


'''
@mazes_app.get("/items/", response_model=list[ schemas.Item ])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
'''

if __name__ == "__main__" :
    import uvicorn

    uvicorn.run("main:mazes_app", log_level="info", reload=True, port=8000)
