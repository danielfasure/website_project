from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from database import engine
from models import Base
from routerfolder.auth_users import router 
from routerfolder import library_handler
from fastapi.middleware.cors import CORSMiddleware
library_router= library_handler.router
app = FastAPI()
origins = [
    "http://localhost:5173", # Default Vite port
]

Base.metadata.create_all(bind=engine)
templates =Jinja2Templates(directory="../frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def test(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})
app.include_router(library_router)
app.include_router(router)