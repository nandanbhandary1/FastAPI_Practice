from fastapi import FastAPI, Depends, HTTPException, status, Path
import models
from database import engine, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field

app = FastAPI()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo_id(db: db_dependency, todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/todo-create", status_code=status.HTTP_201_CREATED)
async def create_book(db: db_dependency, todo_req: TodoRequest):
    todo_model = Todos(**todo_req.model_dump())  # CONVERT REQ TO MODEL
    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_request:TodoRequest, to_id:int=Path(ge=1)):
    todo_model = db.query(Todos).filter(Todos.id == to_id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
    