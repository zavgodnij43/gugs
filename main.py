from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(title="Library API")

# Тимчасове сховище
library = {}


class Book(BaseModel):
    titel: str = Field(
        ...,
        title="Назва книги",
        description="Обов'язкове поле",
        min_length=1
    )
    pages: int = Field(
        ...,
        title="Кількість сторінок",
        description="Обов'язкове поле",
        gt=10,
        le=1000
    )
    author: str = Field(
        ...,
        title="Ім'я автора",
        description="Обов'язкове поле",
        min_length=5
    )


class Message(BaseModel):
    message: str


@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    author = book.author
    if author not in library:
        library[author] = []
    library[author].append(book)
    return book


@app.get("/books/", response_model=list[Book])
async def get_books(author: str = Query(..., title="Автор")):
    if author not in library:
        raise HTTPException(status_code=404,detail="Автор не знайдений")
    return library[author]


@app.put("/books/", response_model=Message)
async def update_book(book: Book):

    if book.author not in library:
        raise HTTPException(
            status_code=404,
            detail="Автора не знайдено"
        )

    for b in library[book.author]:
        if b.titel == book.titel:
            b.pages = book.pages
            return {"message": "Книга оновлена"}
    raise HTTPException(status_code=404,detail="Книгу не знайдено")


@app.delete("/books/", response_model=Message)
async def delete_book(titel: str = Query(...),author: str = Query(...)):
    if author not in library:
        raise HTTPException(
            status_code=404,
            detail="Автора не знайдено"
        )
    for b in library[author]:
        if b.titel == titel:
            library[author].remove(b)
            if not library[author]:
                del library[author]
            return {
                "message": f"Книгу '{titel}' успішно видалено"
            }
    raise HTTPException(
        status_code=404,
        detail="Книгу не знайдено"
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )