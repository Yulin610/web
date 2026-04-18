# Stage V4 Completion Report (Advanced Features)

## 1) Stage V4 Goal
实现高级能力，用于拉开 70 与 80+ 的差距：
- 搜索功能
- 统计 API
- 数据库索引
- API Key 安全机制
- 请求日志系统

## 2) Implemented Features

### 2.1 Search (Implemented)
在统一列表接口中增加搜索参数：
- `GET /books?search=harry`

实现细节：
- 在 `app/services/book_service.py` 中对 `title` 做大小写不敏感匹配。
- 与已有 `author/sort/order/page/size` 可同时使用。

### 2.2 Stats APIs (Implemented)
新增路由：`app/routes/stats.py`

已实现接口：
- `GET /stats/average-rating`
  - 返回全库平均评分
- `GET /stats/top-books?limit=10`
  - 返回评分最高图书列表
- `GET /stats/books-per-year`
  - 从 `publication_date` 解析年份，统计各年份图书数

服务层实现：
- `app/services/stats_service.py`

### 2.3 Database Indexes (Implemented)
按任务要求创建并保证现有库可落地：
- `CREATE INDEX IF NOT EXISTS idx_title ON books(title);`
- `CREATE INDEX IF NOT EXISTS idx_rating ON books(average_rating);`

位置：
- `app/main.py` 启动阶段执行

说明：
- 数据列名实际为 `average_rating`，因此 `idx_rating` 建在该列上。

### 2.4 API Key Security (Implemented)
新增简单鉴权机制：
- Header: `x-api-key`
- 默认密钥：`cw1-secret-key`
- 可由环境变量 `BOOKS_API_KEY` 覆盖

实现：
- `app/security/api_key.py`
- 在 `books` 与 `stats` 路由上统一挂载依赖

行为：
- 缺失或错误 key -> `401 Unauthorized`
- 错误格式：
```json
{
  "success": false,
  "message": "Invalid or missing API key"
}
```

### 2.5 Logging System (Implemented)
在 `app/main.py` 增加 HTTP middleware，记录：
- 请求路径
- 状态码
- 耗时（ms）

日志示例（本地测试）：
- `path=/books status=200 duration_ms=...`

## 3) Verification Summary
本地冒烟测试已通过：
- `GET /books?page=1&size=3&search=harry` -> 200
- `GET /stats/average-rating` -> 200
- `GET /stats/top-books?limit=2` -> 200
- `GET /stats/books-per-year` -> 200
- 不带 API key 调用业务接口 -> 401

同时验证索引存在：
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

