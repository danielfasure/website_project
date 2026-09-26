from fastapi import APIRouter, Depends,HTTPException,Request,Query
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates


from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from routerfolder.auth_users import get_current_user,redirect_to_login

from database import get_db
from models import User,Librarys,Books,Authors
from schemas.model_validate import Library_maker,books_maker,Authors_maker
router = APIRouter(prefix="/admin",
    tags=["admin"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]

###endpoints 
@router.delete("/delete_library/{libraryid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(libraryid:int,user:user_depedency,db:db_dependency):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail="user  is not an admin or not found")
    library_model = db.query(Librarys).filter(Librarys.id==libraryid).first()
    if library_model is None:
        raise HTTPException(status_code=404,detail='library not found')
    db.query(Librarys).filter(Librarys.id==libraryid).delete()
    db.commit()

@router.post("/add_book")
async def add_book(db:db_dependency,bookmaker:books_maker,library:int,request:Request):
    user = await get_current_user(request.cookies.get('access_token'))
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail="user not found")
    if library is None:
        raise HTTPException(status_code=404,detail="stoppppppp")
    book_model=Books(**bookmaker.model_dump())

    book_model.libraryid=library
    db.add(book_model)
    db.commit()

@router.post("/add_library")
async def add_library(db:db_dependency,library_request:Library_maker,request:Request):
    user = await get_current_user(request.cookies.get('access_token'))

    if user is None or user.get('role')!='admin':
        
        raise HTTPException(status_code=401,detail="user not found")
    library_model = Librarys(**library_request.model_dump())
    db.add(library_model)
    db.commit()    

@router.put("/update_library/{libraryid}")
async def add_library(db:db_dependency,user_db:user_depedency,library_request:Library_maker,libraryid:int):
    library_model = user_db.query(Librarys).filter(Librarys.id==libraryid).first()
    if library_model is not None:
        raise HTTPException(status_code=404,detail='library not found')
    
    library_model.name =library_request.name
    library_model.postcode = library_request.postcode
    library_model.capacity = library_request.capacity 
    db.add(library_model)
    db.commit()    



    