from fastapi import APIRouter
from services.service import service
from pydantic import BaseModel


class OrderResponse(BaseModel):
    pass


router = APIRouter(prefix="/api/v1/orders")


@router.get("", response_model=OrderResponse)
async def get_orders() -> OrderResponse:
    return service.get_orders()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str) -> OrderResponse:
    return service.get_order(order_id)


@router.delete("/cancel-order}")
async def cancel_order():
    return service.cancel_order()
