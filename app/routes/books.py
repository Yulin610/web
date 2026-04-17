from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, PaginatedBooksResponse, SuccessResponse
from app.services.book_service import list_books

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=PaginatedBooksResponse)
def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    author: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    try:
        books, total = list_books(
            db, page=page, size=size, author=author, sort=sort, order=order
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {
        "success": True,
        "data": [BookResponse.model_validate(b) for b in books],
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/{book_id}", response_model=SuccessResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return {"success": True, "data": BookResponse.model_validate(book)}


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"success": True, "data": BookResponse.model_validate(book)}


@router.put("/{book_id}", response_model=SuccessResponse)
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    for k, v in payload.model_dump().items():
        setattr(book, k, v)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"success": True, "data": BookResponse.model_validate(book)}


@router.delete("/{book_id}", response_model=SuccessResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    db.delete(book)
    db.commit()
    return {"success": True, "data": {"deleted": True, "id": book_id}}
