from fastapi import Depends, status, Path, HTTPException, Response, APIRouter
import models
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field

router = APIRouter()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}")
async def read_todo_id(db: db_dependency, todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Not found")


@router.post("/todo-create", status_code=status.HTTP_201_CREATED)
async def create_book(db: db_dependency, todo_req: TodoRequest):
    todo_model = Todos(**todo_req.model_dump())  # CONVERT REQ TO MODEL
    db.add(todo_model)
    db.commit()


@router.put("/todoo{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(ge=1)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todooo/{todoo_id}")
async def delete_todo(db: db_dependency, todoo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todoo_id).first()
    if not todo_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="todo not found"
        )
    db.query(Todos).filter(Todos.id == todoo_id).delete()
    db.commit()
    return Response(content="BOOK DELETED", status_code=status.HTTP_204_NO_CONTENT)

