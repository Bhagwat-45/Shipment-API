from typing import Annotated
from sqlalchemy import create_engine
from fastapi import Depends
from sqlmodel import SQLModel, Session

engine = create_engine(
    url="sqlite:///shipments_db.db",
    echo=True,
    connect_args={
        "check_same_thread" : False
    }
)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session,Depends(get_session)]