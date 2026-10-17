from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from pydantic import BaseModel
from services.customer.customers import get_all_customers, get_customer 


router = APIRouter(prefix="/api/v1/customers", tags=["customers"])


@router.get("/", status_code=200)
async def customers(db: AsyncSession = Depends(get_db)):
    return await get_all_customers(db=db)

@router.get("/{customer_id}", status_code=200)
async def customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    return await get_customer(customer_id=customer_id, db=db)