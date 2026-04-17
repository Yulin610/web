from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.book import Book


ALLOWED_SORT_FIELDS = {
    "id": Book.id,
    "title": Book.title,
    "average_rating": Book.average_rating,
    "ratings_count": Book.ratings_count,
    "num_pages": Book.num_pages,
    "publication_date": Book.publication_date,
    "publisher": Book.publisher,
}


def list_books(
    db: Session,
    *,
    page: int,
    size: int,
    author: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
) -> Tuple[list[Book], int]:
    if page < 1 or size < 1:
        raise ValueError("page and size must be positive integers")

    sort_col = ALLOWED_SORT_FIELDS.get(sort)
    if sort_col is None:
        raise ValueError(f"Invalid sort field: {sort}")

    q = db.query(Book)

    if author:
        author = author.strip()
        if author:
            # SQLite doesn't support ILIKE; use lower() comparison.
            q = q.filter(func.lower(Book.authors).like(f"%{author.lower()}%"))

    total = q.count()

    order = (order or "asc").lower()
    if order not in {"asc", "desc"}:
        raise ValueError("order must be 'asc' or 'desc'")

    q = q.order_by(sort_col.asc() if order == "asc" else sort_col.desc())
    q = q.offset((page - 1) * size).limit(size)

    return q.all(), total

