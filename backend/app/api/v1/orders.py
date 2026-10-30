from fastapi import APIRouter
from services.orders.orders import get_orders, get_order_by_id
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.db import get_db
from uuid import UUID
from schemas.schema import Order, OrderResponse


router = APIRouter(prefix="/api/v1/orders")


@router.get("/customer/{customer_id}", response_model=list[OrderResponse]) ## response_model=OrderResponse --- removed it for now
async def handle_get_orders(
    customer_id: UUID,  
    db: AsyncSession = Depends(get_db),
    ):
    return await get_orders(customer_id=customer_id, db=db)


@router.get("/{customer_id}/{order_id}", response_model=OrderResponse)
async def handle_get_order(
    customer_id: UUID, 
    order_id: UUID, 
    db: AsyncSession = Depends(get_db)):
    return await get_order_by_id(order_id=order_id, customer_id=customer_id, db=db)


# @router.delete("/cancel-order}")
# async def cancel_order():
#     return service.cancel_order()
