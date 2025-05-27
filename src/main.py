from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router
from src.settings import settings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)