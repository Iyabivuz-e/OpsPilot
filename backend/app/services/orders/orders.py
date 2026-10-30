from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from helpers.current_logged import get_current_user
from models.models import Order, User
from database.db import get_db
from uuid import UUID


# Get all orders for the current user
async def get_orders(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
) -> list[Order]:
    """
    Get all orders for the current user.
    """
    
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    try:
        orders = db.query(Order).filter(
            Order.customer_id == user.id
            ).offset(offset).limit(limit).all()
        
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get the order by ID for the current user    
async def get_order_by_id(
    order_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Order:
    
    """Get a specific order by ID for the current user."""
    
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.customer_id == user.id
        ).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))