# Stage V1 Completion Report (MVP) — superseded by V2

## 1) Project Theme and Data Source
- Selected theme: **Books**
- Dataset used: `archive/books.csv`
- Dataset background: Goodreads API scraped book metadata dataset (Kaggle-style public dataset description provided in task brief)

### Data compatibility check (sampled)
Sampled columns from CSV:
- `bookID`
- `title`
- `authors`
- `average_rating`
- `isbn`
- `language_code`
- `num_pages` (in file header appears as `  num_pages`)
- `ratings_count`
- `publication_date`
- `publisher`

The MVP data model was aligned to these columns to ensure import and query consistency.

## 2) Tech Stack Selection and Rationale
- **FastAPI**: fast delivery for REST APIs, automatic OpenAPI/Swagger support, concise Python code for coursework MVP.
- **SQLite**: zero-config SQL database, easy local setup for marking and demonstrations.
- **SQLAlchemy**: clean ORM mapping for `Book` table and CRUD operations.

This stack balances simplicity, correctness, and extensibility for later stages (V2/V3/V4).

## 3) MVP Development Scope Delivered

### Implemented database/model
- SQLite database file: `books.db`
- Table: `books`
- ORM model: `app/models/book.py`

### Data import
- Script: `import_books.py`
- Input: `archive/books.csv`
- Behavior:
  - creates DB/table if missing
  - cleans numeric fields (`bookID`, `average_rating`, `num_pages`, `ratings_count`)
  - imports rows into `books`

### Required 4 APIs delivered
- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `DELETE /books/{id}`

Routes file: `app/routes/books.py`  
App entry: `app/main.py`

## 4) MVP Acceptance Check

### Runtime
- Server starts via:
  - `uvicorn app.main:app --reload`
- Health endpoint:
  - `GET /` returns JSON message

### Data availability
- CSV import succeeded locally.
- Imported row count check: `11127` records in `books` table.

### API smoke test evidence
Automated local test (FastAPI TestClient) results:
- `GET /books` -> `200`
- `GET /books/1` -> `200`
- `POST /books` -> `201`
- `DELETE /books/{new_id}` -> `204`

Result: **Stage V1 minimum requirements met** (service runnable, JSON responses, data query works).

## Notice
Stage V2 implementation and the updated report are available in:
- `archive/reports/V2_Completion_Report.md`

## 5) GenAI Usage Statement (Required)
GenAI was used in this stage for:
- identifying/structuring implementation steps from coursework requirements
- drafting FastAPI + SQLAlchemy boilerplate
- drafting CSV import and basic data cleaning logic
- generating project report text

All outputs were manually verified against the dataset and tested locally before finalizing.

## 6) Files Produced in Stage V1
- `requirements.txt`
- `app/main.py`
- `app/database/connection.py`
- `app/models/book.py`
- `app/schemas/book.py`
- `app/routes/books.py`
- `import_books.py`
- `README.md`
- `archive/reports/V1_Completion_Report.md`
