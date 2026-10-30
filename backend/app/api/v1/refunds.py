from fastapi import APIRouter
from services.refunds.refunds import get_refunds_for_customer
from pydantic import BaseModel


class RefundResponse(BaseModel):
    pass


router = APIRouter(prefix="/api/v1/refunds")


@router.get("/{customer_id}", response_model=RefundResponse)
async def get_refunds(customer_id: str) -> RefundResponse:
    return await get_refunds_for_customer(customer_id=customer_id)


# @router.get("/eligibility", response_model=RefundResponse)
# async def get_refund_eligibility() -> RefundResponse:
#     return service.get_refund_eligibility()


# @router.get("/{payment_id}", response_model=RefundResponse)
# async def get_refunds(payment_id: str) -> RefundResponse:
#     return service.get_payment(payment_id)
