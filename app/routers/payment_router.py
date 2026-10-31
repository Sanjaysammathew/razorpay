from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.payment_schema import CreateOrderRequest, PaymentCreatedResponse, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-order", response_model=PaymentCreatedResponse, status_code=201)
async def create_order(payload: CreateOrderRequest, session: AsyncSession = Depends(get_db)):
    payment = await PaymentService(session).create_order(payload.product_id)
    return PaymentCreatedResponse(
        payment_id=payment.id,
        razorpay_order_id=payment.razorpay_order_id,
        amount=payment.amount,
        currency=payment.currency,
    )


@router.get("", response_model=list[PaymentResponse])
async def list_payments(session: AsyncSession = Depends(get_db)):
    return await PaymentService(session).list_payments()


@router.get("/razorpay-order/{order_id}")
async def get_razorpay_order(order_id: str, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    return await PaymentService(session).get_razorpay_order(order_id)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, session: AsyncSession = Depends(get_db)):
    return await PaymentService(session).get_payment(payment_id)
