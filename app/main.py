from fastapi import FastAPI, HTTPException, Query, status
from app.database import get_media, get_media_by_id, get_copies, create_loan as create_loan_db, return_loan as return_loan_db
from app.database import create_media as create_media_db, update_media as update_media_db, delete_media as delete_media_db
from app.database import get_loans as get_loans_db, get_active_loans
from typing import List
from app.models import Media, Availability, MediaCreate, Copy, MediaUpdate, LoanCreate

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

@app.patch("/media/{media_id}")
def update_media(media_id: int, media: MediaUpdate):
     if not media.model_dump(exclude_unset=True):
          raise HTTPException(
               status_code=400,
               detail="At least one field must be provided"
          )
     result = update_media_db(media_id, media)
     if result is None:
          raise HTTPException(status_code=404, detail="Media Not Found")
     return result

@app.delete("/media/{media_id}", status_code=204)
def delete_media(media_id: int):
     result = delete_media_db(media_id)

     if result is None:
          raise HTTPException(
               status_code=404,
               detail="Media Not Found"
          )

@app.post("/loans", status_code=201)
def create_loan(loan: LoanCreate):
    result = create_loan_db(loan)

    if result == "COPY_NOT_FOUND":
        raise HTTPException(
             status_code=404,
             detail="Copy not found"
        )

    if result == "USER_NOT_FOUND":
         raise HTTPException(
              status_code=404,
              detail="User not found"
         )

    if result is None:
        raise HTTPException(
            status_code=409,
            detail="Copy is already checkout out"
        )
    return result

@app.post("/loans/{loan_id}/return")
def return_loan(loan_id: int):
     result = return_loan_db(loan_id)

     if result is None:
          raise HTTPException(
               status_code=404,
               detail="Loan not found or already returned"
          )
     return result

@app.get("/loans")
def get_loans():
     return get_loans_db()

@app.get("/loans/active")
def get_active_loans_endpoint():
     return get_active_loans()