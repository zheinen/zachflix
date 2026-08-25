from pydantic import BaseModel

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