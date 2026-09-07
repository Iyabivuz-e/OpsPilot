from fastapi import APIRouter
from services.service import service
from pydantic import BaseModel

class RefundResponse(BaseModel):
    pass


router = APIRouter(prefix="/api/v1/refunds")


@router.get("/", response_model=RefundResponse)
async def get_refunds() -> RefundResponse:
    return service.get_refunds()


@router.get("/eligibility", response_model=RefundResponse)
async def get_refund_eligibility() -> RefundResponse:
    return service.get_refund_eligibility()


@router.get("/{payment_id}", response_model=RefundResponse)
async def get_refunds(payment_id: str) -> RefundResponse:
    return service.get_payment(payment_id)
