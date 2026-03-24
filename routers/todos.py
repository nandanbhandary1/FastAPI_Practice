from fastapi import Depends, status, Path, HTTPException, Response, APIRouter
from database.database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from database.models import Todos
from pydantic import BaseModel, Field
from dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/todo", tags=["todo"])


def get_db():
    db = sessionLocal()  # Opens connection to database
    try:
        yield db  # Sends this db to your route function
    finally:
        db.close()  # Closes connection


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]  # MAKE API AUTHENTICATED


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(db: db_dependency, user: user_dependency):
    # return db.query(Todos).all()
    # print(user)
    # print(user["sub"])
    # print(user["id"])
    # return {"msg": "All todos here"}
    return (
        db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    )  # GET TODOS FOR ONLY PARTICULAR USER


@router.get("/{todo_id}")
async def read_todo_id(db: db_dependency, user: user_dependency, todo_id):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(db: db_dependency, todo_req: TodoRequest, user: user_dependency):
    todo_model = Todos(
        **todo_req.model_dump(), owner_id=user.get("id")
    )  # CONVERT REQ TO MODEL
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest,user:user_dependency, todo_id: int = Path(ge=1)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
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


@router.delete("/{todo_id}")
async def delete_todo(db: db_dependency,user:user_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if not todo_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="todo not found"
        )
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return Response(content="BOOK DELETED", status_code=status.HTTP_204_NO_CONTENT)
