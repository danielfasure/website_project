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
template = Jinja2Templates(directory="../frontend/webpages")
router = APIRouter(prefix="/lib",
    tags=["lib"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]
### pages
@router.get("/book-page")
async def render_book_page(
    request: Request,
    db: db_dependency,
    library_id: int = Query(...)
):
    user = await get_current_user(request.cookies.get('access_token'))

    if not user:
        return template.TemplateResponse("login.html", {"request": request})

    library = db.query(Librarys).filter(Librarys.id == library_id).first()

    if not library:
        raise HTTPException(status_code=404, detail="Library not found")

    library_books = db.query(Books).filter(Books.libraryid == library_id).all()

    return template.TemplateResponse("library_book.html", {
        "request": request,
        "library": library,
        "library_book": library_books,
        "user": user
    })




### endpoint
@router.get("/showcase")
def get_library(db:db_dependency,user:user_depedency ):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     return db.query(Librarys).all

@router.get("/showcase/{libraryid}")
async def get_library(db:db_dependency,libraryid:int,user:user_depedency):
     if user is None:
        raise HTTPException(status_code=401,detail="user not found")
     current_library = db.query(Librarys).filter(Librarys.id==libraryid).first()
     if current_library is not None:
        return current_library
     raise HTTPException(status_code=404, detail='libraries not found ')
    


@router.post("/add_library")
async def add_library(db:db_dependency,user:user_depedency,library_request:Library_maker):
    if user is None:
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

@router.delete("/delete_library/{libraryid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(libraryid:int,user_db:user_depedency,db:db_dependency):
    library_model = db.query(Librarys).filter(Librarys.id==libraryid).first()
    if library_model is not None:
        raise HTTPException(status_code=404,detail='library not found')
    db.query(Librarys).filter(Librarys.id==libraryid).delete()
    db.commit()
    

