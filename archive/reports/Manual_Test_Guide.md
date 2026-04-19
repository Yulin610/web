# Manual Test Guide (Books API V4)

This document provides **manual testing examples** (Swagger / Postman / PowerShell) based on real rows in `books.db`.

## 0) Pre-check: database samples (from `books.db`)
- Total rows: `11127`
- Stable sample IDs: `1`, `2`, `4`, `5`, `8`, `10`
- `author=Rowling` matches: e.g. ids `1/2/4/5/8/10`
- `search=harry` matches: e.g. ids `1/2/4/5/8/9/10`
- Publication year distribution (top): `2006, 2005, 2004, 2003, 2002 ...`

## 1) Test environment setup

### 1.1 Start the server
```bash
uvicorn app.main:app --reload
```

### 1.2 Base URL
- `http://127.0.0.1:8000`

### 1.3 Swagger
- `http://127.0.0.1:8000/docs`

### 1.4 API key (required for business endpoints)
- Header name: `x-api-key`
- Default value: `cw1-secret-key`
- Optional override (environment variable):
```bash
set BOOKS_API_KEY=your_key
```

> Note: `/` does not require API key. Most `/books` and `/stats` endpoints require it.

---

## 2) Authentication tests

### 2.1 Health check (no API key required)
- **Request**: `GET /`
- **Expected**: `200 OK`
- **Expected JSON contains**: `{"message":"Books API is running"}`

### 2.2 Missing API key should be rejected
- **Request**: `GET /books?page=1&size=1`
- **Expected**: `401 Unauthorized`
- **Expected JSON contains**:
```json
{ "success": false, "message": "Invalid or missing API key" }
```

---

## 3) Books API tests (CRUD + pagination + filter/sort + search)

> For all requests below, include header: `x-api-key: cw1-secret-key`

### 3.1 List books (pagination)
- **Request**: `GET /books?page=1&size=5`
- **Expected**: `200 OK`
- **Checks**:
  - `success == true`
  - `data` is an array (length around 5)
  - response includes `total`, `page`, `size`

### 3.2 Filter by author
- **Request**: `GET /books?author=Rowling&page=1&size=5`
- **Expected**: `200 OK`
- **Checks**:
  - returned `data[i].authors` contains `Rowling` (e.g., book id 1/2/4)

### 3.3 Search by title keyword
- **Request**: `GET /books?search=harry&page=1&size=5`
- **Expected**: `200 OK`
- **Checks**:
  - returned `data[i].title` contains `Harry` (e.g., book id 1/2/4/5/8)

### 3.4 Sort results
- **Request**: `GET /books?page=1&size=5&sort=average_rating&order=desc`
- **Expected**: `200 OK`
- **Checks**:
  - `data[0].average_rating >= data[1].average_rating` (descending)

### 3.5 Invalid sort field should return 400
- **Request**: `GET /books?sort=not_a_field`
- **Expected**: `400 Bad Request`
- **Checks**:
  - `success == false`
  - `message` indicates invalid sort field

### 3.6 Get a book by ID (exists)
- **Request**: `GET /books/1`
- **Expected**: `200 OK`
- **Checks**:
  - `data.id == 1`
  - title is a Harry Potter entry

### 3.7 Get a book by ID (not exists)
- **Request**: `GET /books/999999999`
- **Expected**: `404 Not Found`
- **Expected JSON contains**:
```json
{ "success": false, "message": "Book not found" }
```

### 3.8 Create a new book
- **Request**: `POST /books`
- **Expected**: `201 Created`
- **Body**:
```json
{
  "title": "Manual Test Book",
  "authors": "Tester",
  "average_rating": 4.2,
  "isbn": "TEST-001",
  "language_code": "eng",
  "num_pages": 123,
  "ratings_count": 10,
  "publication_date": "4/18/2026",
  "publisher": "QA Press"
}
```
- **Checks**:
  - response includes `data.id` (save it as `{new_id}` for PUT/DELETE)

### 3.9 Validation error should return 400
- **Request**: `POST /books`
- **Expected**: `400 Bad Request`
- **Body**:
```json
{
  "title": " ",
  "authors": "Tester",
  "average_rating": 6
}
```
- **Checks**:
  - `success == false`
  - `message == "Bad Request"`
  - response has `errors`

### 3.10 Update the created book
- **Request**: `PUT /books/{new_id}`
- **Expected**: `200 OK`
- **Body**:
```json
{
  "title": "Manual Test Book Updated",
  "authors": "Tester Updated",
  "average_rating": 4.8
}
```
- **Checks**:
  - returned `data.title == "Manual Test Book Updated"`

### 3.11 Delete the created book
- **Request**: `DELETE /books/{new_id}`
- **Expected**: `200 OK`
- **Expected JSON contains**:
```json
{
  "success": true,
  "data": { "deleted": true, "id": 123 }
}
```

### 3.12 Confirm delete
- **Request**: `GET /books/{new_id}`
- **Expected**: `404 Not Found`

---

## 4) Stats API tests

> For all requests below, include header: `x-api-key: cw1-secret-key`

### 4.1 Average rating
- **Request**: `GET /stats/average-rating`
- **Expected**: `200 OK`
- **Checks**:
  - JSON has `data.average_rating` (number)

### 4.2 Top books
- **Request**: `GET /stats/top-books?limit=5`
- **Expected**: `200 OK`
- **Checks**:
  - `data` array length is 5
  - items have high `average_rating` (often close to 5.0)

### 4.3 Books per year
- **Request**: `GET /stats/books-per-year`
- **Expected**: `200 OK`
- **Checks**:
  - `data` is an array
  - each item has `year` and `count`
  - common years include `2006/2005/2004`

---

## 5) PowerShell quick commands

```powershell
$base = "http://127.0.0.1:8000"
$h = @{ "x-api-key" = "cw1-secret-key" }

# Pagination list
Invoke-RestMethod -Method Get -Uri "$base/books?page=1&size=3" -Headers $h

# Search
Invoke-RestMethod -Method Get -Uri "$base/books?search=harry&page=1&size=3" -Headers $h

# Get by id
Invoke-RestMethod -Method Get -Uri "$base/books/1" -Headers $h

# Stats
Invoke-RestMethod -Method Get -Uri "$base/stats/average-rating" -Headers $h
```

