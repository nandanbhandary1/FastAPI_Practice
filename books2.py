from fastapi import FastAPI, Body, Path, Query, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

books = []


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_year: int,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="ID is not needed when creating", default=None
    )
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=10, max_length=100)
    rating: int = Field(gt=0, le=5)
    published_year: int = Field(gt=1900, lt=2027)

    model_config = {  # DUMMY DATA TO DISPLAY IN SWAGGER API ORDER DOESN'T MATTER WILL ARRARGE BASED ON ALPHABETIC
        "json_schema_extra": {
            "example": {
                "title": "Title one",
                "author": "Nandan",
                "description": "Dummy",
                "rating": 5,
                "published_year": 2020,
            }
        }
    }


BOOKS = [
    Book(1, "Batman", "Nandan", "Action Movie", 5, 2003),
    Book(2, "Spider Man", "Nandan", "Movie", 4, 1995),
    Book(3, "3 idiots", "Smrithika", "Life lesson", 3, 2025),
    Book(4, "Jab we met", "Smrithika", "Love", 2, 1999),
    Book(5, "Hridayam", "Smrithi", "Love", 2, 2003),
]


@app.get("/books/publish")
async def read_books_by_year(year: int):
    result = []
    for book in BOOKS:
        if book.published_year == year:
            result.append(book)
    return result


def next_id():
    if len(BOOKS) == 0:
        return 1
    else:
        return BOOKS[-1].id + 1


@app.get("/books")
async def read_books():
    return BOOKS


@app.post("/books/create")
async def create_book(new_book: BookRequest):
    print(type(new_book))
    hosa_book = Book(**new_book.model_dump())  # USED TO CONVERT A REQUEST TO OBJECT
    hosa_book.id = next_id()
    BOOKS.append(hosa_book)
    print(type(hosa_book))


@app.get("/fetch{id}")
def fetch_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Id does not exist!"
    )


@app.get("/fetch/query")
def fetch_book_query(rating: int = Query(ge=1, le=5)):
    result = []
    for book in BOOKS:
        if book.rating == rating:
            result.append(book)
    return result


@app.put("/book-update")
async def book_update(ubook: BookRequest):
    book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == ubook.id:
            BOOKS[i] = Book(**ubook.model_dump())
            book_found = True
        if book_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BOOKS



@app.delete("/book-delete")
async def book_delete(dbook: int):
    book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == dbook:
            book_found = True
            BOOKS.pop(i)
        if not book_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BOOKS
