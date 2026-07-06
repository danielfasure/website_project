from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = (
  #  "postgresql://postgres:Ayomikun12!@192.168.1.253:5432/LibrarySystem"
# " postgresql://danieldb:qN0qkxheAAbdvLNuC9Jaha2Y8AFfRuSi@dpg-d8tfpag0697c73ciq3n0-a/library_db_gudm"
#) # this is the url the driver, the username, password, then hostname, then database. 
DATABASE_URL = (
    "postgresql://neondb_owner:npg_EUru3ZKvDz8L@ep-plain-bar-atntu453.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"
   
)

engine = create_engine(DATABASE_URL)# create the connection to the url where this database is stor 
#session local is the factory where the work is done 
# session local has method to  handle the data in the database  
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()# this class can be intheritanted by table we want to be able to store and alter 


def get_db(): # will give you an the instance of the of session but only if session local class can be created 
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close(); 
