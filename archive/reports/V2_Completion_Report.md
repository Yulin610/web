# Stage V2 Completion Report (CRUD + Validation +规范化响应)

## 1) Stage V2 Goal
在 V1 可运行的基础上，使 API **更规范**：
- 补全 CRUD（新增 `PUT /books/{id}`）
- 加入数据验证（Pydantic）
- 状态码符合要求（200/201/400/404）
- 统一响应格式（成功/失败）
- 数据清洗更完善（去重、空值处理、rating 转 float）

## 2) Implemented Changes

### 2.1 CRUD 完整
新增接口：
- `PUT /books/{id}`：更新指定图书

### 2.2 数据验证（Pydantic）
在 `app/schemas/book.py` 中实现：
- `title`：必填且不能是空字符串（`min_length=1` + 去空格校验）
- `average_rating`：范围限制 **0–5**（`ge=0, le=5`）

说明：
- 当请求体不合法时，系统会返回 **400 Bad Request**（见异常处理）。

### 2.3 HTTP 状态码规范
已对齐课程要求：
- `GET /books`：200 OK
- `GET /books/{id}`：200 OK / 404 Not Found
- `POST /books`：201 Created / 400 Bad Request
- `PUT /books/{id}`：200 OK / 400 Bad Request / 404 Not Found
- `DELETE /books/{id}`：200 OK / 404 Not Found

### 2.4 统一响应格式（重要）
成功返回：
```json
{
  "success": true,
  "data": {}
}
```

失败返回：
```json
{
  "success": false,
  "message": "Book not found"
}
```

当请求体校验失败时（400）：
```json
{
  "success": false,
  "message": "Bad Request",
  "errors": [...]
}
```

实现方式：
- 在 `app/main.py` 中增加了全局异常处理：
  - `RequestValidationError` -> 400 + 统一错误结构
  - `HTTPException` -> 404/400 等 + 统一错误结构

### 2.5 数据清洗（导入阶段）
在 `import_books.py` 中增强：
- 去重：按 `bookID` 去重（重复 id 跳过）
- 处理空值：
  - 空 `title`：跳过导入
  - 空 `authors`：写入 `Unknown`
- 数值清洗：
  - `average_rating` -> float
  - `num_pages/ratings_count/bookID` -> int（无法转换则为 None 或跳过）

## 3) Files Changed / Added
- Updated:
  - `app/schemas/book.py`
  - `app/routes/books.py`
  - `app/main.py`
  - `import_books.py`
- Added:
  - `archive/reports/V2_Completion_Report.md`

## 4) GenAI Usage Statement (Required)
GenAI used for:
- V2 requirements mapping into concrete FastAPI implementation tasks
- drafting validation + unified response + exception handler patterns
- drafting report content

All outputs were manually reviewed and executed locally, and adjusted to match `archive/books.csv` fields and coursework rules.

