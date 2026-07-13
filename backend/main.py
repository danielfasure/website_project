import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI,Request

from fastapi.templating import Jinja2Templates
from database import engine
from models import Base
from routerfolder.auth_users import router 
from routerfolder import library_handler
from routerfolder import book_handler
import routerfolder.admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys


library_router= library_handler.router
book_router=book_handler.router
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "frontend", "functionality")
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "frontend", "webpages")


Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Setup Templates using a direct relative string path
templates = Jinja2Templates(directory=TEMPLATES_DIR)
@app.get("/")
def test(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})
app.include_router(library_router)
app.include_router(router)
app.include_router(book_router)
app.include_router(routerfolder.admin.router)
