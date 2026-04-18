# 图书 API 课程作业（V4 增强版）  
基于 FastAPI + SQLite 开发，使用 Goodreads 图书数据集（`archive/books.csv`）。  
  
## 项目与数据集  
- 主题：图书信息 API  
- 数据文件`archive/books.csv`  
- 来源：Goodreads API 公开图书数据  
  
## 技术栈  
- FastAPI：开发高效，内置自动接口文档  
- SQLite：轻量 SQL 数据库，便于演示与评分  
- SQLAlchemy：ORM 数据模型映射  
  
## V1–V4 实现功能  
- 数据库初始化  
- 图书数据模型  
- CSV 数据导入脚本  
- RESTful CRUD（V2 已补全 PUT）：  
  - `GET /books` 获取图书列表  
  - `GET /books/{id}` 获取单本图书  
  - `POST /books` 添加图书  
  - `PUT /books/{id}` 更新图书（V2）  
  - `DELETE /books/{id}` 删除图书  
- 数据校验（V2）：  
  - `title` 必填且不能为空  
  - `average_rating` 范围 0–5  
- 统一响应格式（V2）：  
  - 成功：`{ "success": true, "data": ... }`  
  - 失败：`{ "success": false, "message": "..." }`  
- 分页 + 筛选 + 排序（V3）：  
  - `GET /books?page=1&size=10`  
  - `GET /books?author=Rowling&sort=average_rating&order=desc`  
- 搜索（V4）：  
  - `GET /books?search=harry`  
- 统计接口（V4）：  
  - `GET /stats/average-rating`  
  - `GET /stats/top-books`  
  - `GET /stats/books-per-year`  
- API Key 鉴权（V4）：  
  - 请求头：`x-api-key: cw1-secret-key`（默认值，可用环境变量 `BOOKS_API_KEY` 覆盖）  
- 请求日志（V4）：  
  - 记录请求路径、状态码、耗时（ms）  
- 数据库索引（V4）：  
  - `idx_title` on `title`  
  - `idx_rating` on `average_rating`  
  
## 项目结构  
```  
app/  
  database/  
  models/  
  routes/  
  schemas/  
  services/  
archive/  
  books.csv  
import_books.py  
requirements.txt  
```  
  
## 运行步骤  
1. 安装依赖  
```bash  
pip install -r requirements.txt  
```  
2. 导入数据  
```bash  
python import_books.py  
```  
3. 启动服务  
```bash  
uvicorn app.main:app --reload  
```  
4. 文档地址`http://127.0.0.1:8000/docs`  
  
## API 示例  
- `GET /books?page=1&size=10`：获取图书列表（V3 分页）  
- `GET /books?author=Rowling&sort=average_rating&order=desc`：筛选 + 排序（V3）  
- `GET /books?search=harry`：按标题搜索（V4）  
- `GET /books/{id}`：获取单本图书  
- `POST /books`：添加图书  
- `PUT /books/{id}`：更新图书（V2）  
- `DELETE /books/{id}`：删除图书  
- `GET /stats/average-rating`：全量图书平均评分（V4）  
- `GET /stats/top-books?limit=10`：高评分图书（V4）  
- `GET /stats/books-per-year`：各年份图书数量（V4）  

## 状态码约定（V2）
- 200 OK：查询/更新/删除成功
- 201 Created：创建成功
- 400 Bad Request：请求体参数不合法（例如 `average_rating` 不在 0–5）
- 404 Not Found：资源不存在（例如 id 不存在）

## 列表接口返回格式（V3）
`GET /books` 返回分页结构（外层仍为 `success` 统一响应）：
```json
{
  "success": true,
  "data": [],
  "total": 11127,
  "page": 1,
  "size": 10
}
```

## 鉴权说明（V4）
除根路径 `/` 和文档页面外，业务接口需带 API Key 请求头：
```http
x-api-key: cw1-secret-key
```

可通过环境变量修改默认密钥：
```bash
set BOOKS_API_KEY=your_key
```
  
## AI 使用声明  
使用生成式 AI 辅助生成项目框架、数据导入脚本、API 代码与报告，所有内容均经人工修改、验证并适配数据集。