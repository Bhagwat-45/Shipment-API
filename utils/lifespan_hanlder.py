from contextlib import asynccontextmanager
from rich import panel, print
from fastapi import FastAPI
from database.session import create_db_tables

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Started!",border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("....Stopped!",border_style="red"))
