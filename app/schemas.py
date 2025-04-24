from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Base schema for a health program
class ProgramBase(BaseModel):
    name: str

# Schema used when creating a new program
class ProgramCreate(ProgramBase):
    pass

# Schema used when returning a program from the DB
class Program(ProgramBase):
    id: int

    class Config:
        orm_mode = True  # Allows compatibility with ORM objects like SQLAlchemy models

# Base schema for a client
class ClientBase(BaseModel):
    name: str
    age: int
    gender: str
    contact: str

# Schema used when creating a new client
class ClientCreate(ClientBase):
    pass

# Schema used when returning a client from the DB
class Client(ClientBase):
    id: int
    programs: List[Program] = []  # List of programs the client is enrolled in

    class Config:
        orm_mode = True

# Schema for enrolling a client in a program
class EnrollmentCreate(BaseModel):
    program_id: int
    client_id: int

# Schema for searching a client
class ClientSearch(BaseModel):
    query: str

# Schema for access token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for extracting token payload (e.g., user info)
class TokenData(BaseModel):
    username: Optional[str] = None
