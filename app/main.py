from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import recipes
from db.db import engine 
from db.models import Base


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(recipes.router)
