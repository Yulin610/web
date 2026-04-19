# PPT Generation Prompt (5-minute defense)

Copy the prompt below into your PPT generation tool (e.g., Gamma / Canva / Tome / Copilot PPT).  
Goal: generate a **5-minute defense deck** in **English** (or bilingual if supported), with concise bullets and clear visuals.

---

## Prompt

You are a presentation designer. Create a **10–12 slide** PPTX for a **5-minute coursework defense** about a project called **“Books API (FastAPI + SQLite)”**.

### Style requirements
- Modern, clean, university-friendly style
- Use consistent color theme (navy/blue + light background)
- Large readable fonts
- Each slide max 5 bullet points
- Use diagrams where useful (architecture, DB model, request flow)

### Project facts (must be accurate)
- Stack: **FastAPI**, **SQLite**, **SQLAlchemy**, **Pydantic**
- Dataset: Goodreads books dataset from `archive/books.csv`
- DB: `books.db`, table: `books`
- API base: `http://127.0.0.1:8000`
- Swagger: `/docs`
- Auth: API key header `x-api-key`, default `cw1-secret-key`, override via env var `BOOKS_API_KEY`
- Unified responses:
  - success: `{ "success": true, "data": ... }`
  - error: `{ "success": false, "message": "..." }`
- List endpoint supports: pagination (`page/size`), filter (`author`), sort (`sort/order`), search (`search`)
- Stats endpoints:
  - `GET /stats/average-rating`
  - `GET /stats/top-books?limit=10`
  - `GET /stats/books-per-year`
- Indexes:
  - `idx_title` on `books.title`
  - `idx_rating` on `books.average_rating`
- Logging: middleware logs path/status/duration_ms

### Slides (required content)
1) **Title**: Books API Coursework (name, module, date)
2) **Problem & Goal**: why build this API + what it solves
3) **Dataset**: source, key columns, size (~11k rows), cleaning decisions
4) **Tech stack**: why FastAPI/SQLite/SQLAlchemy
5) **Architecture**: diagram (routes → services → DB); mention structure: `routes/`, `services/`, `models/`, `schemas/`
6) **Database model**: show `Book` entity with main fields
7) **Core API (CRUD)**: endpoints list + status codes
8) **V3 features**: pagination/filter/sort (show example request + response shape with total/page/size)
9) **V4 features**: search + stats + indexes + logging + API key (show one example request for each)
10) **Testing**: mention Swagger + manual test guide + example test cases (401, 400, 404, CRUD)
11) **Version control evidence**: show a timeline V1→V2→V3→V4 and what changed each version
12) **Deliverables**: GitHub repo, API doc PDF, technical report PDF, test guide, how to run

### Demo script notes (speaker notes)
Add brief speaker notes per slide (1–2 sentences) to fit 5 minutes total.

### Include these concrete examples in slides
- `GET /books?page=1&size=10&author=Rowling&sort=average_rating&order=desc`
- `GET /books?search=harry&page=1&size=5`
- `GET /stats/average-rating`

Return the deck outline and generate the PPTX content accordingly.

