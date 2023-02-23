#  Created by btrif Trif on 31-01-2023 , 3:53 PM.
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
from passlib.context import CryptContext

import os
from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt, JWTError

from models import User
from schemas import TokenDataSchema, TokenSchema, oauth2_scheme
from crud import get_user, verify_password
from database import get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 300  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "alpha_Beta_gamma_delta_abcdef_0123456789"  # should be kept secret
# JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret
JWT_REFRESH_SECRET_KEY = "alpha_Beta_gamma_delta_abcdef_0123456789"  # should be kept secret
# JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']    # should be kept secret

pwd_context = CryptContext(schemes=[ "bcrypt" ], deprecated="auto")

##############################################
####                Make and Verify hashed passwords            ####

'''
def get_hashed_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    # return password_context.verify(password, hashed_pass)
    return pbkdf2_sha256.verify(password, hashed_pass)
'''


###############################
####             User functions                 ####

def authenticate_user(db, username: str, password: str) :
    user = get_user(db, username)
    print(f"user : {user}")
    if not user :
        print(f"if not user <-------")
        return False
    if not verify_password(password, user.hashed_password) :
        print(f"if not verify_password <-------")
        print(f"password : {password} <-------")
        print(f"user.hashed_password : {user.hashed_password} <-------")
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) :
    user = fake_decode_token(token)
    return user


def authenticate_user(db, username: str, password: str) :
    user = get_user(db, username)
    if not user :
        return False
    if not verify_password(password, user.hashed_password) :
        return False
    return user


###############################
####             Token functions             ####

def fake_decode_token(token) :
    return User(
            username=token + "fakedecoded", email="john@example.com"
            )


def create_access_token(data: dict, expires_delta: Union[ timedelta, None ] = None) :
    to_encode = data.copy()
    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
        ) :
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate" : "Bearer"},
            )
    try :
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ ALGORITHM ])
        print(f"credentials_exception -> payload : {payload}")
        username: str = payload.get("sub")
        print(f"credentials_exception -> spooky username :  {username}")

        if username is None :
            raise credentials_exception

        token_data = TokenDataSchema(username=username)
        print(f"get_current_user -> token_data : {token_data}")
    except JWTError :
        print(f"get_current_user -> credentials_exception {credentials_exception}")
        raise credentials_exception

    # Get user from DB
    user = get_user(db, token_data.username)
    print(f"get_current_user -> user_from_DB : {user}")
    if user is None :
        print(f"credentials_exception  second {credentials_exception}")
        raise credentials_exception

    return user
