#  Created by btrif Trif on 19-02-2023 , 8:49 PM.
from fastapi import Depends
from sqlalchemy.testing import db

from crud import get_user
import models
import schemas
from database import db_engine
from utils import get_hashed_password, verify_password
from sqlalchemy.orm import Session
import pytest


'''
def get_user(db: Session, user_name: str) :
    return db.query(models.User).filter(models.User.username == user_name).first()
'''

from database import SessionLocal, SQLALCHEMY_DATABASE_URL, Base
from main import get_db

def test_get_user():
    user_name = "evanzo"
    result = get_user(Depends(get_db), user_name)

    assert 1 == 1




