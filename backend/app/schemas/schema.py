import uuid
from enum import StrEnum
from typing import List, Literal
from pydantic import BaseModel, EmailStr, Field
from backend.app.helpers.id_generator import generate_id_code


class RefundReturnStatus(StrEnum):
    REQUESTED = ("REQUESTED",)
    PROCESSING = ("PROCESSING",)
    COMPLETED = ("COMPLETED",)
    FAILED = "FAILED"


class OrderStatus(StrEnum):
    PENDING = ("PENDING",)
    PROCESSING = ("PROCESSING",)
    SHIPPED = ("SHIPPED",)
    DELIVERED = ("DELIVERED",)
    CANCELLED = ("CANCELLED",)
    RETURNED = "RETURNED"


class PaymentStatus(StrEnum):
    CAPTURED = ("CAPTURED",)
    FAILED = ("FAILED",)
    PENDING = ("PENDING",)
    REFUNDED = ("REFUNDED",)
    PARTIALLY_REFUNDED = ("PARTIALLY_REFUNDED",)
    DUPLICATE = "DUPLICATE"


## Pydantic validations
class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: EmailStr
    role: str


class Customer(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: EmailStr
    country: str


class Order(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    order_id: str = Field(
        default_factory=generate_id_code("order")
    )  # The customer Id who placed the order
    customer_id: str
    status: OrderStatus


class Refund(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    refund_id: str = Field(
        default_factory=generate_id_code("refund")
    )  # The customer Id who placed the order
    order_id: str
    payment_id: str
    amount: float
    status: RefundReturnStatus


class Return(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    return_id: str = Field(
        default_factory=generate_id_code("return")
    )  # The customer Id who placed the order
    order_id: str
    reason: str
    status: RefundReturnStatus


class Payment(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    payment_id: str = Field(
        default_factory=generate_id_code("payment")
    )  # The customer Id who placed the order
    order_id: str
    amount: float
    method: str = Field(default_factory="CARD")  # We hardcode it for the moment
    status: PaymentStatus


class Case(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    case_id: str = Field(
        default_factory=generate_id_code("case")
    )  # The customer Id who placed the order
    customer_id: str
    order_id: str
    title: str
    description: str
    # category
    # status
    # priority
    # resolution
    status: List[
        Literal[
            "OPEN",
            "PENDING",
            "CLOSED",
        ]
    ]
