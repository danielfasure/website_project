from fastapi import APIRouter, Depends,HTTPException,Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates


from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from routerfolder.auth_users import get_current_user

from database import get_db
from models import User,Librarys,Books,Authors
from schemas.model_validate import Library_maker,books_maker,Authors_maker
template = Jinja2Templates(directory="../frontend/webpages")
router = APIRouter(prefix="/book",
    tags=["book"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]
###pages 
@router.get("/add_book")
async def add_book(request:Request,library:int,user:user_depedency):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     return template.TemplateResponse("add_book.html",{"request":request,"library":library})
    

###endpoints
@router.get("/userbooks")
async def showcase_books(db:db_dependency,user:user_depedency):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     return db.query(Books).filter(Books.userid==user.get('id')).all()



@router.post("/addbook")
async def add_library(db:db_dependency,user:user_depedency,bookmaker:books_maker,libraryid:int):
    if user is None:
        raise HTTPException(status_code=401,detail="user not found")
    book_model=Books(**bookmaker.model_dump())
    book_model.libraryid=libraryid
    db.add(book_model)
    db.commit()


@router.put("/loanbook/{bookid}")
async def loan_book(db:db_dependency,user:user_depedency,bookid:int):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     
     owned= db.query(Books.id).filter(Books.id==bookid).first()
     if owned is None:
      loandedbook=db.query(Books).filter(Books.id==bookid).first()    
      loandedbook.userid= user.get('id')
     else:
        raise HTTPException(status_code=401,detail="book already owned ")

@router.put("/unloanbook/{bookid}")
async def loan_book(db:db_dependency,user:user_depedency,bookid:int):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     loandedbook=db.query(Books).filter(Books.id==bookid).first()    
     loandedbook.userid= None
     db.add(loandedbook)   
     db.commit()
