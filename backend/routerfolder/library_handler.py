from fastapi import APIRouter, Depends,HTTPException
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
router = APIRouter(prefix="/lib",
    tags=["lib"])

db_dependency = Annotated[Session,Depends(get_db)]
user_depedency = Annotated[Session,Depends(get_current_user)]
### pages






### endpoint
@router.get("./showcase")
def get_library(db:db_dependency, ):
    return db.query(Librarys).all

@router.get("./showcase/{libraryid}")
async def get_library(db:db_dependency,libraryid:int):
    current_library = db.query(Librarys).filter(Librarys.id==libraryid).first()
    if current_library is not None:
        return current_library
    raise HTTPException(status_code=404, detail='libraries not found ')
    


@router.post("/add_library")
async def add_library(db:db_dependency,user_db:user_depedency,library_request:Library_maker):
    library_model = Librarys(**library_request.model_dump())
    user_db.add(library_model)
    user_db.commit()

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
    

