import uuid
from typing import List, Literal
from pydantic import BaseModel, EmailStr, Field
from helpers.code_generator import generate_id_code


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
    id: str = Field(default_factory = generate_id_code("order")) # The customer Id who placed the order
    customer_id: str
    status: List[Literal[
        "PENDING",
        "PROCESSING",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
        "RETURNED"
        ]]
    
class Refund(BaseModel):
    id: str = Field(default_factory = generate_id_code("refund")) # The customer Id who placed the order
    order_id: str
    payment_id: str
    amount: float
    status: List[Literal[
        "REQUESTED",
        "PROCESSING",
        "COMPLETED",
        "FAILED"
        ]]

class Return(BaseModel):
    id: str = Field(default_factory = generate_id_code("return")) # The customer Id who placed the order
    order_id: str
    reason: str
    status: List[Literal[
        "REQUESTED",
        "PROCESSING",
        "COMPLETED",
        "FAILED"
        ]]

class Payment(BaseModel):
    id: str = Field(default_factory = generate_id_code("payment")) # The customer Id who placed the order
    order_id: str
    amount: float
    method: str = Field(default_factory = "CARD") # We hardcode it for the moment 
    status: List[Literal[
        "CAPTURED",
        "FAILED",
        "PENDING",
        "REFUNDED",
        "PARTIALLY_REFUNDED",
        "DUPLICATE"
        ]]
    
class Case(BaseModel):
    id: str = Field(default_factory = generate_id_code("case")) # The customer Id who placed the order
    customer_id: str
    order_id: str
    title: str 
    description: str
    # category
    # status
    # priority
    # resolution
    status: List[Literal[
        "OPEN",
        "PENDING",
        "CLOSED",
        ]]