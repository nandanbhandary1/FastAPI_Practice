from fastapi import FastAPI
import database.models as models
from database.database import engine
from routers import auth, todos

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True}) # KEEP AUTHORIZATION  AFTER PAGE REFRESH

app.include_router(auth.router)
app.include_router(todos.router)


models.Base.metadata.create_all(bind=engine)  # USED TO CREATE A TABLE IN DB
