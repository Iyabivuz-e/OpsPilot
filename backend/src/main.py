from fastapi import FastAPI
from api.v1 import orders_router, payments_router, refunds_router, returns_router

app = FastAPI()

app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(refunds_router)
app.include_router(returns_router)


@app.get("/health")
async def health():
    return {"message": "The app is healthy"}
