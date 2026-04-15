import csv
from pathlib import Path

from app.database.connection import Base, SessionLocal, engine
from app.models.book import Book

CSV_PATH = Path("archive/books.csv")


def clean_int(value: str):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def clean_float(value: str):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def seed_books():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Book).delete()

        seen_ids: set[int] = set()
        with CSV_PATH.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                book_id = clean_int(row.get("bookID"))
                title = (row.get("title") or "").strip()
                authors = (row.get("authors") or "").strip()

                if not title:
                    continue
                if book_id is None:
                    continue
                if book_id in seen_ids:
                    continue
                seen_ids.add(book_id)

                book = Book(
                    id=book_id,
                    title=title,
                    authors=authors or "Unknown",
                    average_rating=clean_float(row.get("average_rating")),
                    isbn=(row.get("isbn") or "").strip() or None,
                    language_code=(row.get("language_code") or "").strip() or None,
                    num_pages=clean_int(row.get("  num_pages")),
                    ratings_count=clean_int(row.get("ratings_count")),
                    publication_date=(row.get("publication_date") or "").strip() or None,
                    publisher=(row.get("publisher") or "").strip() or None,
                )
                db.add(book)

        db.commit()
        print("Books imported successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_books()
