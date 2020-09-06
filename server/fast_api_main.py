import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


class Book(BaseModel):
    title: str
    author: str
    read: bool = False


@app.get("/ping")
def index():
    return "hogehoge"


@app.get("/books")
def all_books():
    return {
        "status": "success",
        "books": BOOKS,
    }


@app.post("/books")
def create_book(book: Book):
    BOOKS.append({
        "id": uuid.uuid4().hex,
        "title": book.title,
        "author": book.author,
        "read": book.read,
    })
    return {
        "status": "success",
        "message": "Book added!",
    }


@app.put("/books/{book_id}")
def edit_book(book_id, book: Book):
    response_object = {
        "status": "success"
    }
    remove_book(book_id)
    BOOKS.append({
        "id": uuid.uuid4().hex,
        "title": book.title,
        "author": book.author,
        "read": book.read,
    })
    response_object["message"] = "Book updated!"
    return response_object


def remove_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return True
    return False


def get_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None
