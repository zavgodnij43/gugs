from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int):
    book_data = book.model_dump() if hasattr(book, "model_dump") else book.dict()
    db_book = models.Book(**book_data, author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_user(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(db: Session, user: schemas.UserCreate, rights: str = "user"):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        login=user.login,
        hashed_password=hashed_password,
        rights=rights
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, login: str, password: str):
    user = get_user(db, login)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user
