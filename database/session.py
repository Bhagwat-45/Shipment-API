from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlmodel import SQLModel
from config.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:   
        await connection.run_sync(SQLModel.metadata.create_all(bind=engine))    
        


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_ = AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession,Depends(get_session)]