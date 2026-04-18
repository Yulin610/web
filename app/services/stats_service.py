from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.book import Book


def get_average_rating(db: Session) -> float:
    avg = db.query(func.avg(Book.average_rating)).scalar()
    return float(avg or 0.0)


def get_top_books(db: Session, limit: int = 10) -> list[Book]:
    return (
        db.query(Book)
        .filter(Book.average_rating.isnot(None))
        .order_by(Book.average_rating.desc(), Book.ratings_count.desc())
        .limit(limit)
        .all()
    )


def get_books_per_year(db: Session) -> list[dict]:
    rows = db.query(Book.publication_date).filter(Book.publication_date.isnot(None)).all()
    per_year = defaultdict(int)
    for (publication_date,) in rows:
        date_text = (publication_date or "").strip()
        if not date_text:
            continue
        parts = date_text.split("/")
        if len(parts) != 3:
            continue
        year = parts[-1]
        if len(year) == 4 and year.isdigit():
            per_year[year] += 1

    return [
        {"year": year, "count": per_year[year]}
        for year in sorted(per_year.keys(), key=int)
    ]
