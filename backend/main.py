from fastapi import FastAPI
from database import engine
from models import Base
from routerfolder.auth_users import router 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)