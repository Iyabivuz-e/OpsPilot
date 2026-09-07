from fastapi import APIRouter
from services.service import service


router = APIRouter(prefix="/api/v1/payments")


@router.get("", response_model=PaymentResponse)
async def get_payments() -> PaymentResponse:
    return service.get_payments()


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payments(payment_id: str) -> PaymentResponse:
    return service.get_payment(payment_id)
