from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateOrderRequest(BaseModel):
    product_id: int


class PaymentCreatedResponse(BaseModel):
    payment_id: int
    razorpay_order_id: str
    amount: int
    currency: str


class PaymentResponse(BaseModel):
    id: int
    product_id: int
    razorpay_order_id: str
    amount: int
    currency: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
