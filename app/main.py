from fastapi import FastAPI, HTTPException, Query
from app.database import get_media, get_media_by_id
from typing import List
from app.models import Media
from app.database import get_copies
from app.models import Copy

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Welcome to ZachFlix!"}

@app.get("/media", response_model=List[Media])
def get_all_media(
    media_type: str | None = Query(None, alias="type"), 
    genre: str | None = None,
    title: str | None = None
    ):
        return get_media(media_type, genre, title)

@app.get("/media/{media_id}", response_model=Media)
def get_one_media(media_id: int):
     media = get_media_by_id(media_id)
     if media is None:
          raise HTTPException(status_code=404, detail="Media Not Found")
     return media

@app.get("/copies", response_model=List[Copy])
def get_all_copies():
    return get_copies()