from pydantic import BaseModel
from enum import Enum

class Media(BaseModel):
    id: int
    title: str
    type: str
    genre: str | None = None
    year: int | None = None

class MediaResponse(BaseModel):
    items: list[Media]
    total: int

class MediaCreate(BaseModel):
    title: str
    type: str
    genre: str
    year: int

class MediaUpdate(BaseModel):
    title: str | None = None
    type: str | None = None
    genre: str | None = None
    year: int | None = None

class Copy(BaseModel):
    title: str
    format: str | None=None
    availability: str

class Availability(str, Enum):
    AVAILABLE = 'AVAILABLE'
    CHECKED_OUT = 'CHECKED OUT'

class LoanCreate(BaseModel):
    copy_id: int
    user_id: int