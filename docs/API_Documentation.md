# Books API Documentation 

## 1. Overview
- **Project**: Books API (Coursework)
- **Framework**: FastAPI
- **Database**: SQLite (`books.db`)
- **Dataset**: `archive/books.csv` (Goodreads books dataset)
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger UI**: `/docs`

## 2. Authentication (API Key)
All business endpoints require an API key.

- **Header name**: `x-api-key`
- **Default key**: `cw1-secret-key`
- **Override**: environment variable `BOOKS_API_KEY`

Example header:
```http
x-api-key: cw1-secret-key
```

Unauthorized response:
- **Status**: `401 Unauthorized`
```json
{ "success": false, "message": "Invalid or missing API key" }
```

## 3. Response Format (Unified)

### 3.1 Success
```json
{ "success": true, "data": {} }
```

### 3.2 Error
```json
{ "success": false, "message": "..." }
```

### 3.3 Validation error (Bad Request)
- **Status**: `400 Bad Request`
```json
{
  "success": false,
  "message": "Bad Request",
  "errors": []
}
```

## 4. Data Model (Book)

### 4.1 Fields
- `id` (int, server-generated for created records; imported from CSV `bookID`)
- `title` (string, required, non-empty)
- `authors` (string, required)
- `average_rating` (float, optional, 0–5)
- `isbn` (string, optional)
- `language_code` (string, optional)
- `num_pages` (int, optional)
- `ratings_count` (int, optional)
- `publication_date` (string, optional, e.g. `9/16/2006`)
- `publisher` (string, optional)

## 5. Endpoints

> All requests below require header `x-api-key`.

### 5.1 Health Check
- **GET** `/`
- **Auth**: not required
- **200 OK** example:
```json
{ "message": "Books API is running" }
```

---

### 5.2 List Books (pagination + filter/sort + search)
- **GET** `/books`

#### Query parameters
- `page` (int, default 1, min 1)
- `size` (int, default 10, min 1, max 100)
- `author` (string, optional; substring match on `authors`)
- `search` (string, optional; substring match on `title`)
- `sort` (string, default `id`)
  - allowed: `id`, `title`, `average_rating`, `ratings_count`, `num_pages`, `publication_date`, `publisher`
- `order` (string, default `asc`)
  - allowed: `asc`, `desc`

#### Request examples
- Pagination:
  - `GET /books?page=1&size=10`
- Filter + sort:
  - `GET /books?author=Rowling&sort=average_rating&order=desc&page=1&size=10`
- Search:
  - `GET /books?search=harry&page=1&size=10`

#### 200 OK response example
```json
{
  "success": true,
  "data": [],
  "total": 11127,
  "page": 1,
  "size": 10
}
```

#### Error codes
- `400 Bad Request`: invalid `sort/order` etc.
- `401 Unauthorized`: missing/invalid API key

---

### 5.3 Get Book by ID
- **GET** `/books/{id}`

#### Path parameters
- `id` (int)

#### 200 OK response example
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Harry Potter ...",
    "authors": "J.K. Rowling",
    "average_rating": 4.57
  }
}
```

#### 404 Not Found
```json
{ "success": false, "message": "Book not found" }
```

---

### 5.4 Create Book
- **POST** `/books`
- **Status**: `201 Created`

#### JSON body
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

#### 201 Created response example
```json
{
  "success": true,
  "data": { "id": 45643, "title": "Manual Test Book", "authors": "Tester" }
}
```

#### Error codes
- `400 Bad Request`: validation error (e.g., empty title, rating out of range)
- `401 Unauthorized`

---

### 5.5 Update Book
- **PUT** `/books/{id}`
- **Status**: `200 OK`

#### JSON body
```json
{
  "title": "Updated Title",
  "authors": "Updated Author",
  "average_rating": 4.8
}
```

#### 200 OK response (same wrapper)

#### Error codes
- `400 Bad Request`
- `401 Unauthorized`
- `404 Not Found`

---

### 5.6 Delete Book
- **DELETE** `/books/{id}`
- **Status**: `200 OK`

#### 200 OK response example
```json
{
  "success": true,
  "data": { "deleted": true, "id": 123 }
}
```

#### Error codes
- `401 Unauthorized`
- `404 Not Found`

---

## 6. Stats Endpoints

### 6.1 Average Rating
- **GET** `/stats/average-rating`
- **200 OK** example:
```json
{
  "success": true,
  "data": { "average_rating": 3.98 }
}
```

### 6.2 Top Books
- **GET** `/stats/top-books`

#### Query parameters
- `limit` (int, default 10, min 1, max 50)

#### 200 OK response example
```json
{
  "success": true,
  "data": [
    { "id": 17224, "title": "The Diamond Color Meditation...", "average_rating": 5.0 }
  ]
}
```

### 6.3 Books Per Year
- **GET** `/stats/books-per-year`
- **200 OK** example:
```json
{
  "success": true,
  "data": [
    { "year": "2006", "count": 1700 },
    { "year": "2005", "count": 1260 }
  ]
}
```

## 7. Related Testing Guide
Manual testing steps (Swagger/Postman/PowerShell) are documented in:
- `archive/reports/Manual_Test_Guide.md`

