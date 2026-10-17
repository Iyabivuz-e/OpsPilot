from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.models import Customer
from sqlalchemy import select


async def get_all_customers(
    skip:int = 0, limit:int = 50,
    db: AsyncSession = Depends(get_db)):
    """
    Retrieve all customers.
    """
    stmt = select(Customer).offset(skip).limit(limit)
    results = await db.scalars(stmt)
    customers = results.all()
    
    if not customers:
        raise HTTPException(status_code=404, detail="Oops, we didn't find any ):")
    return customers

async def get_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a customer by their ID.
    """
    stmt = select(Customer).where(Customer.id == customer_id)
    customer = await db.scalar(stmt)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
