import logging
import time

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database.connection import Base, engine
from app.routes.books import router as books_router
from app.routes.stats import router as stats_router

Base.metadata.create_all(bind=engine)
with engine.begin() as conn:
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_title ON books(title)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_rating ON books(average_rating)"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("books-api")

app = FastAPI(title="Books API", version="4.0.0")
app.include_router(books_router)
app.include_router(stats_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "path=%s status=%s duration_ms=%.2f",
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Bad Request",
            "errors": jsonable_encoder(exc.errors()),
        },
    )


@app.get("/")
def health_check():
    return {"message": "Books API is running"}
