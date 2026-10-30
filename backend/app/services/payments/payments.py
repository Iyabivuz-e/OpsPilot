from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
# from helpers.current_logged import get_current_user
from models.models import Payment
from database.db import get_db
from uuid import UUID


# Get all payments for the specified customer
async def get_customer_payments(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
) -> list[Payment]:
    """
    Get all payments for the specified customer.
    """
    
    # if not customer:
    #     raise HTTPException(status_code=401, detail="Customer not authenticated")
    
    try:
        payments = db.query(Payment).filter(
            Payment.customer_id == customer_id
            ).offset(offset).limit(limit).all()
        
        if not payments:
            raise HTTPException(status_code=404, detail="No payments found for this customer")  
        
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Get the payment by order ID for the specified customer    
async def get_payment_for_order(
    order_id: UUID,
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Payment:
    
    """Get a specific order by ID for the current customer."""
    
    # if not customer:
    #     raise HTTPException(status_code=401, detail="Customer not authenticated")

    try:
        order_payment = db.query(Payment).filter(
            Payment.order_id == order_id,
            Payment.customer_id == customer_id
        ).first()

        if not order_payment:
            raise HTTPException(status_code=404, detail="Payment for this order not found")

        return order_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))