from sqlalchemy import create_engine  # → Creates a connection to your database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos-app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tiger@localhost/TodoAppDatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

Base = declarative_base()


# sessionmaker
# → Used to create sessions (connections) to perform operations like:

# insert
# update
# delete
# query


# declarative_base
# → Used to create a base class for models (tables)
# → All your tables will inherit from this
