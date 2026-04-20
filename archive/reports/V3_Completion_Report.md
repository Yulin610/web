# Stage V3 Completion Report (RESTful + Pagination + Filter/Sort + Modularization)

## 1) Stage V3 Goal
Bring the project to a **submission-ready** level:
- Unified RESTful design (consistent routes)
- Pagination on list endpoint (`page`/`size` with `total/page/size` in the response)
- Filtering + sorting combined on `GET /books`
- Clear modular structure (introduce `services/`)
- Swagger available via FastAPI (`/docs`)

## 2) RESTful API Design (Implemented)
Unified routes:
- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `PUT /books/{id}`
- `DELETE /books/{id}`

## 3) Pagination (Implemented)
Endpoint:
- `GET /books?page=1&size=10`

Return shape:
```json
{
  "success": true,
  "data": [...],
  "total": 11127,
  "page": 1,
  "size": 10
}
```

Constraints:
- `page >= 1`
- `size` default 10, max 100

## 4) Filter + Sort (Implemented)
Single endpoint combining filter and sort:
- Filter by author substring:
  - `GET /books?author=Rowling`
- Sort + order:
  - `GET /books?sort=average_rating&order=desc`

Allowed sort fields:
- `id`, `title`, `average_rating`, `ratings_count`, `num_pages`, `publication_date`, `publisher`

Invalid `sort` or `order` returns **400 Bad Request** with unified error response.

## 5) Modular Structure (Implemented)
Added a service layer:
- `app/services/book_service.py`

Responsibilities:
- build SQLAlchemy queries (pagination/filter/sort)
- return `(items, total)` back to the routes layer

Project structure now includes:
```
app/
  database/
  models/
  routes/
  schemas/
  services/
```

## 6) Swagger / OpenAPI
- Available at: `http://127.0.0.1:8000/docs`

## 7) Files Changed / Added (V3)
- Added:
  - `app/services/book_service.py`
  - `app/services/__init__.py`
  - `archive/reports/V3_Completion_Report.md`
- Updated:
  - `app/routes/books.py` (pagination/filter/sort)
  - `app/schemas/book.py` (paginated response schema)
  - `app/main.py` (version bump)
  - `README.md` (V3 usage)

## 8) GenAI Usage Statement (Required)
GenAI used for:
- translating V3 requirements into route/query/service design
- drafting pagination + filter/sort patterns for SQLAlchemy + FastAPI
- drafting the V3 completion report

All outputs were manually reviewed and tested locally.

## 9) Deliverables & Links
- **GitHub repository**: `https://github.com/Yulin610/web`
- **API documentation (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/API_Documentation.pdf`
- **Technical report (PDF)**: `https://github.com/Yulin610/web/blob/main/docs/Technical_Report.pdf`
- **Defense PPT (PPTX)**: `https://github.com/Yulin610/web/blob/main/docs/Books_API_Coursework_Defense.pptx`

