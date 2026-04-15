from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    authors: str
    average_rating: Optional[float] = Field(default=None, ge=0, le=5)
    isbn: Optional[str] = None
    language_code: Optional[str] = None
    num_pages: Optional[int] = None
    ratings_count: Optional[int] = None
    publication_date: Optional[str] = None
    publisher: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("title is required")
        return v


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[Any] = None
