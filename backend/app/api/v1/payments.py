from fastapi import APIRouter
from services.payments.payments import get_customer_payments, get_payment_for_order
from pydantic import BaseModel


class PaymentResponse(BaseModel):
    pass


router = APIRouter(prefix="/api/v1/payments")


@router.get("", response_model=PaymentResponse)
async def get_payments() -> PaymentResponse:
    return await get_customer_payments()


# @router.get("/{payment_id}", response_model=PaymentResponse)
# async def get_payments(payment_id: str) -> PaymentResponse:
#     return get_payment_for_order(payment_id)
