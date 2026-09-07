from fastapi import APIRouter
from services.service import service
from pydantic import BaseModel


class PaymentResponse(BaseModel):
    pass


router = APIRouter(prefix="/api/v1/returns")


@router.get("/", response_model=PaymentResponse)
async def get_returns() -> PaymentResponse:
    return service.get_returns()


@router.get("/{return_id}", response_model=PaymentResponse)
async def get_refunds(return_id: str) -> PaymentResponse:
    return service.get_return(return_id)
