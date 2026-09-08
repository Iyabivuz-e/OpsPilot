from fastapi import FastAPI
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

app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(refunds_router)
app.include_router(returns_router)
app.include_router(login_router)


@app.get("/health")
async def health():
    return {"message": "The app is healthy"}
