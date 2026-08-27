from pydantic import BaseModel
from enum import Enum

class Media(BaseModel):
    id: int
    title: str
    type: str
    genre: str | None = None
    year: int | None = None

class Copy(BaseModel):
    title: str
    format: str | None=None
    availability: str

class Availability(str, Enum):
    AVAILABLE = 'AVAILABLE'
    CHECKED_OUT = 'CHECKED OUT'