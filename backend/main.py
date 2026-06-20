from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from database import engine
from models import Base
from routerfolder.auth_users import router 
from routerfolder import library_handler
from routerfolder import book_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
library_router= library_handler.router
book_router=book_handler.router
app = FastAPI()


Base.metadata.create_all(bind=engine)
templates =Jinja2Templates(directory="../frontend/webpages")
app.mount("/frontend/static",StaticFiles(directory="../frontend/functionality"),name="static")
@app.get("/")
def test(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})
app.include_router(library_router)
app.include_router(router)
app.include_router(book_router)
