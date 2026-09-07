from fastapi import APIRouter
from services.service import service


router = APIRouter(prefix="/api/v1/refunds")


@router.get("/", response_model=PaymentResponse)
async def get_refunds() -> PaymentResponse:
    return service.get_refunds()


@router.get("/eligibility", response_model=PaymentResponse)
async def get_refund_eligibility() -> PaymentResponse:
    return service.get_refund_eligibility()


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_refunds(payment_id: str) -> PaymentResponse:
    return service.get_payment(payment_id)
