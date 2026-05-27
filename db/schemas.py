from typing import Union
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: Union[str, None] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    login: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    rights: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
