#  Created by btrif Trif on 31-01-2023 , 3:56 PM.
import subprocess
from datetime import datetime
from logging import debug

from fastapi.responses import RedirectResponse

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import SessionLocal, db_engine

models.Base.metadata.create_all(bind=db_engine)

mazes_app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


@mazes_app.post("/users/", response_model=schemas.User)
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
@mazes_app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)) :
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None :
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
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
@mazes_app.get("/hello_user")
async def hello_user(
        username: str,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
        ) :
    db_user = crud.get_user(db, user_name=username)
    if db_user is None :
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message" : {
            "Hello" : db_user,
            }
        }


@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs() :
    return RedirectResponse(url='/docs')



'''
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
        ) :
    # user = fake_decode_token(token)
    user = crud.get_user(db, user_name=token)
    # if user is None :
    #     raise HTTPException(status_code=404, detail="User not found")

    if not user :
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate" : "Bearer"},
                )
    return user
'''


## Without this Athorization button does not work !
@mazes_app.post("/login")
async def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        # token: str = Depends(oauth2_scheme)
        ) :

    # 1.  Get the user from DB
    user = crud.get_user(db, user_name=form_data.username)
    if user is None :
        raise HTTPException(status_code=404, detail="User not found")
    print(f"user : {user.email}   'passwd: ' {user.hashed_password}")

    # 2. Check password :
    user_passwd = form_data.password
    if not user_passwd == user.hashed_password :
        raise HTTPException(status_code=400, detail="Incorrect password")

    return user



'''
@mazes_app.get("/items/", response_model=list[ schemas.Item ])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
'''

if __name__ == "__main__" :
    import uvicorn

    uvicorn.run("mazes.main:mazes_app", log_level="info", reload=True, port=8000)
