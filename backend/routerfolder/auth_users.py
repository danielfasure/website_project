from fastapi import APIRouter, Depends,HTTPException,Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import get_db
from models import User,Librarys,Books
from schemas.user_validate import UserCreate
from schemas.model_validate import Token
from main import templates
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
SECRET_KEY = "daniellibrarykey"
ALGORITHM = "HS256"
oaut2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

brcrypt_context =CryptContext(schemes=['bcrypt'],deprecated='auto')
db_dependency = Annotated[Session,Depends(get_db)]

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def create_access_token(username: str, user_id: int, email:str,role:str,expires_delta:timedelta):
    encode = {
        "sub": username,
        "id": user_id,"email":email,"role":role,
       }
    expires= datetime.now(timezone.utc)+expires_delta
    
    encode.update({"exp":expires
    })
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)




async def get_current_user(token:Annotated[str,Depends(oaut2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str=payload.get('role')
        user_email:str=payload.get('email')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not valid hhuser')
        return { 'username': username,'id':user_id,'role':user_role,'email':user_email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')




def auth_user(username:str,password:str,db):
    user =db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not brcrypt_context.verify(password,user.hashed_password):
        return False
    return user


user_dependency =Annotated[dict,Depends(get_current_user)]

def redirect_to_login():
    redirect_response =RedirectResponse(url="/auth/login-page")


### pages 

@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
@router.get("/register-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

@router.get("/library-page")
async def render_library_page(request:Request,db:db_dependency):

    try:
        user =await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return templates.TemplateResponse("login.html",{"request":request})
        
        library= db.query(Librarys).all()
        if library is None:
            templates.TemplateResponse("librarypage.html",{"request":request,"user":user})

        return templates.TemplateResponse("librarypage.html",{"request":request,"libraries":library,"user":user})

    except:
        return redirect_to_login()       
    




###endpoint 







@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreate):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone=create_user_request.phone_number,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name
    )

    db.add(create_user_model)
    db.commit()



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = auth_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token( username=user.username, user_id=user.id, role=user.role,email=user.email, expires_delta=timedelta(minutes=60))

    return {'access_token': token, 'token_type': 'bearer'}    

@router.get("/get_users")
async def retrieve_user(user:user_dependency,db:db_dependency):
    if user is None:
         raise HTTPException(status_code=401,detail="user not found")
    return db.query(User).all()