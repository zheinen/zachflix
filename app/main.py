from fastapi import FastAPI, HTTPException, Query, status
from app.database import get_media, get_media_by_id, get_copies, create_media as create_media_db
from typing import List
from app.models import Media, Availability, MediaCreate, Copy

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
def get_all_copies(
     title: str | None = None,
     availability: Availability | None = None
):
    return get_copies(title, availability.value if availability else None)

@app.post("/media", response_model=Media, status_code=status.HTTP_201_CREATED)
def create_media(media: MediaCreate):
     return create_media_db(media)