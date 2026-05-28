from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session


from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from routerfolder.auth_users import get_current_user

from database import get_db
from models import User,Librarys
router = APIRouter(prefix="/auth",
    tags=["Auth"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]
