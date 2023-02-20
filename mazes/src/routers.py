#  Created by btrif Trif on 20-02-2023 , 11:20 PM.

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session



from fastapi import APIRouter

router = APIRouter()


