from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import (
    orders_router,
    payments_router,
    refunds_router,
    returns_router,
    login_router,
)
from database.db import create_tables
from core.settings import settings
from contextlib import asynccontextmanager
from helpers.errors import AppExceptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    yield
print(f"the db is connected")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=settings.CORS_HEADERS,
)

@app.exception_handler(AppExceptions)
async def app_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )
    
@app.exception_handler(RequestValidationError)
async def app_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input",
            }
        }
    )
    

app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(refunds_router)
app.include_router(returns_router)
app.include_router(login_router)


@app.get("/health")
async def health():
    return {"message": "The app is healthy"}
