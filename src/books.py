from fastapi import FastAPI, Body

app = FastAPI()


books = [
    {"title": "title1", "author": "Nandan", "cate": "math"},
    {"title": "title2", "author": "Nandan", "cate": "phy"},
    {"title": "title3", "author": "Smrithika", "cate": "science"},
    {"title": "title4", "author": "Smrithika", "cate": "bioo"},
]


@app.get("/booksss")
async def first_api():
    return books


@app.get("/books/{bookK}")
async def read_all_books(bookK: str):
    for book in books:
        if book["title"].lower() == bookK.lower():
            return book
    return {"param": book}


@app.get("/books/mybook")
async def read_all():
    return {"njdn"}


@app.get("/books")
async def read_category(cat: str):
    result = []
    for book in books:
        if book["cate"].lower() == cat.lower():
            result.append(book)
    return result


@app.get("/books/{author}")
async def read_book_cat(author: str, cate: str):
    result = []
    for book in books:
        if (
            book["author"].lower() == author.lower()
            and book["cate"].lower() == cate.lower()
        ):
            result.append(book)
    return result


@app.post("/books/create")
async def create_book(new_book=Body()):
    books.append(new_book)


@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(books)):
        if books[i]["title"].lower() == updated_book["title"].lower():
            books[i] = updated_book
            return {"message": "Message "}
    return {"message": "Not found"}


@app.delete("/books/delete/{titlee}")
async def delete(titlee: str):
    for i in range(len(books)):
        if books[i]["title"].lower() == titlee.lower():
            books.pop(i)
            return {"msg": "Delete hogaya"}
    return {"msg": "Not found"}


@app.get("/fetchall/{author}")
async def fetch_all(author: str):
    result = []
    for book in books:
        if book["author"].lower() == author.lower():
            result.append(book)
    return result

@app.get('/fetchquery/')
async def fetch_query(query):
    result = []
    for book in books:
        if book["author"].lower() == query.lower():
            result.append(book)
    return result 