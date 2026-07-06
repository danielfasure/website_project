import os
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

router = APIRouter(prefix="/book",
    tags=["book"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]
ROUTER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROUTER_DIR, "..", "..", "frontend", "webpages")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

###pages 

@router.get("/add_book")
async def add_book(request:Request,library:int,):
     user = await get_current_user(request.cookies.get('access_token'))
     if user is None:
           raise HTTPException(status_code=401,detail="user not found")
     return templates.TemplateResponse("add_book.html",{"request":request,"library":library})
    

###endpoints
@router.get("/userbooks")
async def showcase_books(db:db_dependency,request:Request):
     user = await get_current_user(request.cookies.get('access_token'))
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     return db.query(Books).filter(Books.userid==user.get('id')).all()



@router.post("/addbook")
async def add_library(db:db_dependency,bookmaker:books_maker,library:int,request:Request):
    user = await get_current_user(request.cookies.get('access_token'))
    if user is None:
        raise HTTPException(status_code=401,detail="user not found")
    book_model=Books(**bookmaker.model_dump())
    book_model.libraryid=library
    db.add(book_model)
    db.commit()


@router.put("/loanbook/{bookid}")
async def loan_book(db:db_dependency,bookid:int,request:Request):
     
     user = await get_current_user(request.cookies.get('access_token'))
     if user is None:
        raise HTTPException(status_code=401,detail="user not found") 
     
     book = db.query(Books).filter(Books.id == bookid).first()

     if not book:
      raise HTTPException(404, "Book not found")

     if book.userid is not None:
      raise HTTPException(400, "Book already owned")
     book.userid = user.get('id')
     db.commit()
    

@router.put("/unloanbook/{bookid}")
async def loan_book(db:db_dependency,bookid:int,request:Request):
     user = await get_current_user(request.cookies.get('access_token'))
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     loandedbook=db.query(Books).filter(Books.id==bookid).first()    
     if not loandedbook:
         raise(HTTPException(404,"book not found "))
     loandedbook.userid= None
     db.add(loandedbook)   
     db.commit()
