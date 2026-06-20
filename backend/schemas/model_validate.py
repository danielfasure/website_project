from pydantic import BaseModel, EmailStr


class Library_maker(BaseModel):
    name: str 
    postcode: str
    capacity: int 
    

class Authors_maker(BaseModel):
    name: str 
    


class books_maker(BaseModel):
    name: str 
  

class Token(BaseModel):
    access_token: str
    token_type: str
