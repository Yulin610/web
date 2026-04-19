# Technical Report

## 1. Project Summary
This project implements a **Books REST API** for coursework, using a public Goodreads books dataset (`archive/books.csv`). The API supports CRUD operations and several advanced features (pagination, filtering/sorting, search, statistics endpoints, API-key security, indexes, and request logging).

## 2. Architecture & Design

### 2.1 High-level architecture
- **FastAPI app layer**: request routing + validation + OpenAPI/Swagger generation
- **Service layer**: query composition and non-trivial logic (pagination/filter/sort/search; stats)
- **Persistence layer**: SQLAlchemy ORM models stored in SQLite

### 2.2 Project structure
```
app/
  main.py                 # app, middleware, exception handlers, index creation
  database/connection.py  # engine + SessionLocal + Base
  models/book.py          # Book ORM model
  schemas/book.py         # Pydantic schemas + unified response models
  routes/
    books.py              # /books endpoints
    stats.py              # /stats endpoints
  services/
    book_service.py       # list_books: pagination/filter/sort/search
    stats_service.py      # average/top-books/books-per-year
  security/api_key.py     # x-api-key auth dependency
import_books.py           # CSV import + cleaning
archive/reports/          # reports + manual test guide
docs/                     # API doc + technical report (export to PDF)
```

### 2.3 Database model
Main table: `books`
- Primary key: `id`
- Notable columns:
  - `title`, `authors`
  - `average_rating`, `ratings_count`, `num_pages`
  - `publication_date`, `publisher`

### 2.4 API design principles
- **RESTful**: standard CRUD routes (`/books`, `/books/{id}`)
- **Consistent errors**: unified JSON error wrapper
- **Stateless auth**: API key header
- **Scalable list endpoint**: pagination + filter/sort/search combined on `GET /books`

## 3. Technology Choices (and Why)

### 3.1 FastAPI
- Rapid development for coursework timeline
- Built-in OpenAPI/Swagger (`/docs`) reduces documentation overhead
- Pydantic integration for request validation

### 3.2 SQLite
- Zero external dependency for markers
- Simple local run and data seeding
- Suitable for MVP and demonstration environment

### 3.3 SQLAlchemy
- Clear ORM mapping from Python class to SQL table
- Easy query composition for pagination/filtering

## 4. Data Source & Import Pipeline

### 4.1 Dataset
- File: `archive/books.csv`
- Origin: Goodreads dataset (scraped via Goodreads API; public dataset description provided in brief)

### 4.2 Cleaning decisions (import stage)
Implemented in `import_books.py`:
- Numeric parsing:
  - `bookID` -> int
  - `average_rating` -> float
  - `num_pages`, `ratings_count` -> int
- Basic integrity rules:
  - skip empty `title`
  - `authors` default to `Unknown` if empty
- De-duplication:
  - skip duplicate `bookID`

## 5. Key Problems Encountered & Solutions

### 5.1 Validation status code mismatch
- **Problem**: FastAPI default validation errors are `422 Unprocessable Entity`, but coursework required `400 Bad Request`.
- **Solution**: Added global `RequestValidationError` handler to return `400` with unified error wrapper.

### 5.2 JSON serialization error in validation details
- **Problem**: Pydantic validation errors may include objects not JSON-serializable (e.g., embedded `ValueError` in context).
- **Solution**: Used `jsonable_encoder()` to safely encode error details before returning.

### 5.3 SQLite index changes not applied to existing DB
- **Problem**: Adding indexes in ORM metadata does not automatically retrofit existing SQLite DB tables.
- **Solution**: On startup, executed:
  - `CREATE INDEX IF NOT EXISTS idx_title ON books(title)`
  - `CREATE INDEX IF NOT EXISTS idx_rating ON books(average_rating)`

## 6. Testing Approach

### 6.1 Automated smoke tests (local)
Used local scripted requests (FastAPI TestClient) to verify:
- CRUD status codes (200/201/400/404)
- pagination/filter/sort/search behavior
- stats endpoints outputs
- API key enforcement (401 on missing key)

### 6.2 Manual testing (for demonstration/marking)
Manual test steps and examples are documented in:
- `archive/reports/Manual_Test_Guide.md`

## 7. Limitations & Future Improvements
- **Pagination performance**: current `total` uses `.count()` which can be costly for very large tables; could optimize with cached counts or approximate counts.
- **Search**: currently uses a simple LIKE search on title; could extend to multi-field search and full-text search (FTS).
- **Publication year parsing**: derives year by splitting `publication_date` string; could normalize to a proper `DATE` type in DB.
- **Auth**: simple API key header; could extend to OAuth2/JWT and role-based access.
- **Observability**: current logging prints path/status/duration; could add structured JSON logs and request IDs.

## 8. GenAI Usage Declaration (Required)
GenAI was used to assist with:
- translating coursework requirements into implementation steps
- drafting FastAPI/SQLAlchemy boilerplate and route skeletons
- drafting CSV import + cleaning logic
- drafting documentation (API docs, technical report, test guide)

All generated outputs were manually reviewed, executed locally, and adjusted to match the dataset fields and coursework requirements.

### 8.1 Conversation log appendix
Cursor conversation transcript (for appendix / evidence):
- [Coursework implementation transcript](7746746a-951f-4f86-bf95-08fad4e63e8e)

