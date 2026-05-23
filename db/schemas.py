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