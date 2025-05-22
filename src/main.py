from fastapi import FastAPI
from src.api import router
from src.settings import settings


app = FastAPI()
app.include_router(router)