from fastapi import FastAPI
from api.v1 import orders_router, payments_router, refunds_router, returns_router
from database.db import get_db

app = FastAPI()

print(f"the db is connected: {get_db()}")


app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(refunds_router)
app.include_router(returns_router)


@app.get("/health")
async def health():
    return {"message": "The app is healthy"}
