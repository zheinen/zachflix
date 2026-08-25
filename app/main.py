from fastapi import FastAPI
from app.database import get_media
from typing import List
from app.models import Media

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Welcome to ZachFlix!"}

@app.get("/media", response_model=List[Media])
def get_all_media():
    return get_media()