from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database.connection import Base, engine
from app.routes.books import router as books_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API", version="3.0.0")
app.include_router(books_router)


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
