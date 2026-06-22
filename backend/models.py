from sqlalchemy import (# we can add table characteristic to represent the attribute in a class 
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship



from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role=Column(String)
    phone=Column(String)
    first_name=Column(String)
    last_name=Column(String)

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    book_author = Column(String)

    authorid = Column(Integer,ForeignKey("authors.id"))
    libraryid = Column(Integer,ForeignKey("librarys.id"))
    userid=Column(Integer,ForeignKey("users.id"))
   
   
class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)




class Librarys(Base):    
    __tablename__ = "librarys"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    postcode = Column(String)
    capacity = Column(Integer)



