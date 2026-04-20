# Stage V2 Completion Report (CRUD + Validation + Unified Responses)

## 1) Stage V2 Goal
Starting from the runnable V1 MVP, Stage V2 aims to make the API **correct and consistent** (coursework-quality):
- Complete CRUD by adding `PUT /books/{id}`
- Add request validation (Pydantic)
- Follow required HTTP status codes (200/201/400/404)
- Use a unified JSON response wrapper for both success and error
- Improve import-time data cleaning (deduplication, null handling, numeric casting)

## 2) Implemented Changes

### 2.1 Complete CRUD
Added:
- `PUT /books/{id}`: update an existing book

### 2.2 Validation (Pydantic)
Implemented in `app/schemas/book.py`:
- `title`: required and must not be blank (min length + strip validation)
- `average_rating`: must be within **0–5** (`ge=0, le=5`)

Behavior:
- Invalid request bodies return **400 Bad Request** (coursework requirement).

### 2.3 HTTP status codes
Aligned with coursework requirements:
- `GET /books`: `200 OK`
- `GET /books/{id}`: `200 OK` / `404 Not Found`
- `POST /books`: `201 Created` / `400 Bad Request`
- `PUT /books/{id}`: `200 OK` / `400 Bad Request` / `404 Not Found`
- `DELETE /books/{id}`: `200 OK` / `404 Not Found`

### 2.4 Unified response wrapper (important)
Success:
```json
{
  "success": true,
  "data": {}
}
```

Error (example):
```json
{
  "success": false,
  "message": "Book not found"
}
```

Validation error (400):
```json
{
  "success": false,
  "message": "Bad Request",
  "errors": []
}
```

Implementation:
- Added global exception handlers in `app/main.py`:
  - `RequestValidationError` -> `400` with unified structure
  - `HTTPException` -> `404/400/...` with unified structure

### 2.5 Import-time data cleaning
Enhanced in `import_books.py`:
- Deduplication: skip duplicate `bookID`
- Null/empty handling:
  - skip empty `title`
  - default empty `authors` to `Unknown`
- Numeric casting:
  - `average_rating` -> float
  - `num_pages/ratings_count/bookID` -> int (fallback to None or skip invalid rows)

## 3) Files Changed / Added
- Updated:
  - `app/schemas/book.py`
  - `app/routes/books.py`
  - `app/main.py`
  - `import_books.py`
- Added:
  - `archive/reports/V2_Completion_Report.md`

## 4) Deliverables & Links
- **GitHub repository**: `https://github.com/Yulin610/web`
- **API documentation (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/API_Documentation.pdf`
- **Technical report (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/Technical_Report.pdf`
- **Defense PPT (PPTX)**: `https://github.com/Yulin610/web/blob/main/docs/Books_API_Coursework_Defense.pptx`

## 5) GenAI Usage Statement (Required)
GenAI was used for:
- mapping V2 requirements into concrete FastAPI tasks
- drafting validation + unified response + exception-handler patterns
- drafting report content

All outputs were manually reviewed and executed locally, and adjusted to match `archive/books.csv` fields and coursework rules.

