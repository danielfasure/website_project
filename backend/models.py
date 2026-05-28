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
    password = Column(String)

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    library_id = Column(
        Integer,
        ForeignKey("librarys.id")
    )

    auth_id = Column(
        Integer,
        ForeignKey("authors.id")
    )

    library = relationship(
        "Librarys",
        back_populates="books"
    )

    author = relationship(
        "Authors",
        back_populates="books"
    )
   
class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship(
        "Books",
        back_populates="author"
    )



class Librarys(Base):    
    __tablename__ = "librarys"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    postcode = Column(String)
    capacity = Column(Integer)

    books = relationship(
        "Books",
        back_populates="library"
    )



