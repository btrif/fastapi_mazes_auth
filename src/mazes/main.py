#  Created by btrif Trif on 31-01-2023 , 3:56 PM.
import subprocess
from datetime import datetime

from fastapi.responses import RedirectResponse

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

mazes_app = FastAPI()


#############################################
#                                   ROUTES

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@mazes_app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@mazes_app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@mazes_app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@mazes_app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@mazes_app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


###############################


@mazes_app.get("/hello")
async def hello_world():
    # return {"message": "Hello World"}

    date = datetime.now().strftime("%d.%m.%Y")
    time = datetime.now().strftime("%H:%M")
    processor = str(subprocess.check_output(["wmic", "cpu", "get", "name"]).strip()).split('\\n')[1]

    return {"message": {"Hello": "World",
                        "Today is": date,
                        "and the time is": time,
                        "processor": processor}}


@mazes_app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


'''
@awesome_mazes.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = db.get(data.email, None)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    # db[data.email] = user    # saving user to database
    return user

'''

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run("main:root", debug=True, reload=True, factory=True)
    uvicorn.run("maze.main:mazes_app", reload=True, port=8000)
