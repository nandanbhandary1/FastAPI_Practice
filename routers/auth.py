from typing import Annotated
from database.database import sessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from pydantic import BaseModel, Field
from database.models import users
from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = sessionLocal()  # Opens connection to database
    try:
        yield db  # Sends this db to your route function
    finally:
        db.close()  # Closes connection


db_dependency = Annotated[Session, Depends(get_db)]


class UserCreate(BaseModel):
    email: str = Field(min_length=2, max_length=15)
    username: str = Field(max_length=10)
    first_name: str = Field(max_length=15)
    last_name: str | None = None
    password: str = Field(min_length=5, max_length=20)
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginSuccess(BaseModel):
    access_token: str
    type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def auth(db: db_dependency, create_user: UserCreate):
    # user_model = users(**create_user.model_dump())
    user_model = users(
        email=create_user.email,
        username=create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        hashed_password=bcrypt_context.hash(create_user.password),
        is_active=True,
        role=create_user.role,
    )
    db.add(user_model)
    db.commit()


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})
    return jwt.encode(
        payload, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(users).filter(username == users.username).first()
    if not user:
        return False
    if bcrypt_context.verify(password, user.hashed_password) == True:
        return user
    return False


@router.post("/login", response_model=LoginSuccess)
async def login(db: db_dependency, login: LoginRequest):
    user = authenticate_user(login.username, login.password, db)
    if user == False:
        return "Not Authenticated"

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"type": "Bearer", "access_token": token}
