from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from helpers.current_logged import get_current_user
from models.models import Order, Customer
from database.db import get_db
from uuid import UUID


# Get all orders for the current customer
async def get_orders(
    customer_id: UUID,
    db: AsyncSession,
    offset: int = 0,
    limit: int = 10,
) -> list[Order]:
    """
    Get all orders for the current customer.
    """
    
    # if not :
    #     raise HTTPException(status_code=401, detail="Customer not authenticated")
    
    try:
        stmt = select(Order).where(
            Order.customer_id == customer_id
            ).offset(offset).limit(limit)
        
        orders = await db.execute(stmt)
        
        return orders.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get the order by ID for the current cusotomer    
async def get_order_by_id(
    order_id: UUID,
    customer_id: UUID,
    db: AsyncSession
) -> Order:
    
    """Get a specific order by ID for the current customer."""
    
    # if not customer:
    #     raise HTTPException(status_code=401, detail="Customer not authenticated")

    try:
        stmt = select(Order).where(
            Order.id == order_id,
            Order.customer_id == customer_id
        )
        
        order = await db.execute(stmt)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))