from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.book import BookResponse, SuccessResponse
from app.security.api_key import require_api_key
from app.services.stats_service import (
    get_average_rating,
    get_books_per_year,
    get_top_books,
)

router = APIRouter(prefix="/stats", tags=["stats"], dependencies=[Depends(require_api_key)])


@router.get("/average-rating", response_model=SuccessResponse)
def average_rating(db: Session = Depends(get_db)):
    return {"success": True, "data": {"average_rating": round(get_average_rating(db), 4)}}


@router.get("/top-books", response_model=SuccessResponse)
def top_books(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    books = get_top_books(db, limit=limit)
    return {"success": True, "data": [BookResponse.model_validate(b) for b in books]}


@router.get("/books-per-year", response_model=SuccessResponse)
def books_per_year(db: Session = Depends(get_db)):
    return {"success": True, "data": get_books_per_year(db)}
