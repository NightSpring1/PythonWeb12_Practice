from pydantic import BaseModel, Field
from datetime import date


class ContactIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str | None = Field(min_length=2, max_length=50)
    emails: list[str] | None
    phones: list[str] | None
    birthday: date | None = None
    description: str | None = Field(max_length=300)


class ContactOut(ContactIn):
    id: int

    class Config:
        orm_mode = True
