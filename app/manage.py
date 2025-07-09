from sqlmodel import SQLModel
from app.core.db import engine


def init_db():
    SQLModel.metadata.create_all(engine)

