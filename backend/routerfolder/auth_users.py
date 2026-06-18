from fastapi import APIRouter, Depends,HTTPException,Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates


from database import get_db
from models import User,Librarys
from schemas.user_validate import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
SECRET_KEY = "daniellibrarykey"
ALGORITHM = "HS256"
oaut2_bearer = OAuth2PasswordBearer(tokenUrl="login")

brcrypt_context =CryptContext(schemes=['bcrypt'],deprecated='auto')
db_dependency = Annotated[Session,Depends(get_db)]
template = Jinja2Templates(directory="../frontend/webpages")

### pages 

@router.get("/login-page")
def render_login_page(request:Request):
    return template.TemplateResponse("login.html",{"request":request})
@router.get("/register-page")
def render_login_page(request:Request):
    return template.TemplateResponse("register.html",{"request":request})



###endpoint 


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
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not valid hhuser')
        return { 'username': username,'id':user_id,'role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not dvalid user')




def auth_user(username:str,password:str,db):
    user =db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not brcrypt_context.verify(password,user.hash_password):
        return False
    return user

@router.post("/register")
async def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    hashed_password = bcrypt_context.hash(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User created"
    }

@router.post("/login")
def login_user(user: UserCreate, db: db_dependency):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not bcrypt_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(
        db_user.username,
        db_user.id,
        timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
user_dependency =Annotated[dict,Depends(get_current_user)]

@router.get("/get_library")
async def retrieve_library(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="user not found")
    db.query(Librarys).all()