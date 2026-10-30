from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
# from helpers.current_logged import get_current_user
from models.models import Refund, Order, Customer
from database.db import get_db
from uuid import UUID


async def create_refund():
    """
    Create a new refund.
    """
    pass


# Get all refunds for the specified customer
async def get_refunds_for_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
) -> list[Refund]:
    """
    Get all refunds for the specified customer.
    """
    
    try:
        refunds = db.query(Refund).filter(
            Refund.customer_id == customer_id
            ).offset(offset).limit(limit).all()
        
        if not refunds:
            raise HTTPException(status_code=404, detail="No refunds found for this customer")  
        
        return refunds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get the refund by order ID for the specified customer
async def get_refund_by_order_id(
    order_id: UUID,
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Refund:
    """
    Get a specific refund by order ID for the current customer.
    """
    
    try:
        refund = db.query(Refund).filter(
            Refund.order_id == order_id,
            Refund.customer_id == customer_id
        ).first()

        if not refund:
            raise HTTPException(status_code=404, detail="Refund for this order not found")

        return refund
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
    
def check_refund_eligibility(order: Order, customer: Customer, request_amount: float) -> dict:
    """
    Check if a refund is eligible for the specified order and customer.
    """
    pass