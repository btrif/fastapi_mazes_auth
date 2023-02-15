#  Created by btrif Trif on 31-01-2023 , 3:56 PM.
import subprocess
from datetime import datetime
from logging import debug

from fastapi.responses import RedirectResponse

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

mazes_app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#############################################
#                                   ROUTES

# Dependency
def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


#
#
# @mazes_app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @mazes_app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @mazes_app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @mazes_app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#         user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @mazes_app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


###############################

##########          AUTHENTICATION          ##########
from crud import get_user


def authenticate_user(fake_db, username: str, password: str) :
    user = get_user(fake_db, username)
    if not user :
        return False
    if not verify_password(password, user.hashed_password) :
        return False
    return user


@mazes_app.get("/hello")
async def hello_world() :
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


@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs() :
    return RedirectResponse(url='/docs')


##########################
from schemas import User


async def get_current_user(token: str = Depends(oauth2_scheme)) :
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate" : "Bearer"},
            )
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ ALGORITHM ])
        username: str = payload.get("sub")
        if username is None :
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError :
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None :
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_user)) :
    if current_user.disabled :
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


################        TOKEN       ########
from schemas import Token
from utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from fastapi import status

from datetime import datetime, timedelta
from typing import Union

'''
@mazes_app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) :
    user = authenticate_user(Depends(get_db), form_data.username, form_data.password)

    if not user :
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate" : "Bearer"}, )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub" : user.username}, expires_delta=access_token_expires
            )
    return {"access_token" : access_token, "token_type" : "bearer"}
'''

### THIS IS THE AUTHORIZE BUTTON from docs, the FORM_DATA
@mazes_app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = authenticate_user(Depends(get_db), form_data.username, form_data.password )
    print(f"user_dict : {user_dict}")
    # user_dict = db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect password")

    # return {"access_token": user.username, "token_type": "bearer"}
    return {"access_token": 'yes_man'}


# @mazes_app.post('/signup', summary="Create new user", response_model=UserOut)
# async def create_user(data: UserAuth) :
#     # querying database to check if user already exist
#     user = db.get(data.email, None)
#     if user is not None :
#         raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User with this email already exist"
#                 )
#     user = {
#         'email' : data.email,
#         'password' : get_hashed_password(data.password),
#         'id' : str(uuid4())
#         }
#     # db[data.email] = user    # saving user to database
#     return user




if __name__ == "__main__" :
    import uvicorn

    uvicorn.run("mazes.main:mazes_app", log_level="info", reload=True, port=8000)
