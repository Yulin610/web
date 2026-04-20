# Stage V4 Completion Report (Advanced Features)

## 1) Stage V4 Goal
Demonstrate advanced features (to differentiate higher marks):
- Search
- Statistics APIs
- Database indexes
- API-key security
- Request logging

## 2) Implemented Features

### 2.1 Search (Implemented)
Added a search parameter to the unified list endpoint:
- `GET /books?search=harry`

Details:
- Implemented case-insensitive matching on `title` in `app/services/book_service.py`.
- Can be combined with `author/sort/order/page/size`.

### 2.2 Stats APIs (Implemented)
New router: `app/routes/stats.py`

Implemented endpoints:
- `GET /stats/average-rating`
  - returns average rating across the whole dataset
- `GET /stats/top-books?limit=10`
  - returns the top-rated books list
- `GET /stats/books-per-year`
  - parses year from `publication_date` and aggregates books per year

Service implementation:
- `app/services/stats_service.py`

### 2.3 Database Indexes (Implemented)
Created required indexes and ensured they apply to an existing SQLite DB:
- `CREATE INDEX IF NOT EXISTS idx_title ON books(title);`
- `CREATE INDEX IF NOT EXISTS idx_rating ON books(average_rating);`

Location:
- executed on startup in `app/main.py`

Note:
- The actual rating column is `average_rating`, so `idx_rating` is created on that column.

### 2.4 API Key Security (Implemented)
Added a simple API-key mechanism:
- Header: `x-api-key`
- Default key: `cw1-secret-key`
- Can be overridden by environment variable `BOOKS_API_KEY`

Implementation:
- `app/security/api_key.py`
- applied as a shared dependency on both `books` and `stats` routers

Behavior:
- missing/invalid key -> `401 Unauthorized`
- unified error JSON:
```json
{
  "success": false,
  "message": "Invalid or missing API key"
}
```

### 2.5 Logging System (Implemented)
Added an HTTP middleware in `app/main.py` that logs:
- request path
- status code
- duration (ms)

Example log line:
- `path=/books status=200 duration_ms=...`

## 3) Verification Summary
Local smoke tests passed:
- `GET /books?page=1&size=3&search=harry` -> 200
- `GET /stats/average-rating` -> 200
- `GET /stats/top-books?limit=2` -> 200
- `GET /stats/books-per-year` -> 200
- calling business endpoints without API key -> 401

Indexes verified:
- `idx_title`
- `idx_rating`

## 4) Files Added / Updated (V4)
- Added:
  - `app/security/api_key.py`
  - `app/routes/stats.py`
  - `app/services/stats_service.py`
  - `archive/reports/V4_Completion_Report.md`
- Updated:
  - `app/main.py` (logging + index creation + stats router)
  - `app/routes/books.py` (search + API key dependency)
  - `app/services/book_service.py` (search support)
  - `app/models/book.py` (index declarations)
  - `README.md` (V4 usage/docs)

## 5) GenAI Usage Statement (Required)
GenAI used for:
- mapping V4 requirements into concrete FastAPI implementation tasks
- drafting middleware/security/service patterns
- generating and structuring the V4 report text

All outputs were manually reviewed, executed, and adjusted in the local project.

## 6) Deliverables & Links
- **GitHub repository**: `https://github.com/Yulin610/web`
- **API documentation (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/API_Documentation.pdf`
- **Technical report (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/Technical_Report.pdf`
- **Defense PPT (PPTX)**: `https://github.com/Yulin610/web/blob/main/docs/Books_API_Coursework_Defense.pptx`

