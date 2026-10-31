import asyncio
from decimal import Decimal, InvalidOperation
from typing import Any

from fastapi import HTTPException, status
from razorpay.errors import BadRequestError, GatewayError, ServerError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.razorpay_config import razorpay_client
from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.product_repository import ProductRepository


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.payments = PaymentRepository(session)
        self.products = ProductRepository(session)

    async def create_order(self, product_id: int) -> Payment:
        product = await self.products.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} was not found")

        try:
            amount_paise = int((Decimal(product.price) * 100).quantize(Decimal("1")))
        except (InvalidOperation, ValueError) as exc:
            raise HTTPException(status_code=422, detail="Product has an invalid price") from exc
        if amount_paise <= 0:
            raise HTTPException(status_code=422, detail="Product price must be greater than zero")

        order_data = {"amount": amount_paise, "currency": "INR", "receipt": f"product-{product.id}"}
        try:
            order: dict[str, Any] = await asyncio.to_thread(razorpay_client.order.create, data=order_data)
        except (BadRequestError, GatewayError, ServerError) as exc:
            raise HTTPException(status_code=502, detail=f"Razorpay could not create the order: {exc}") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Razorpay order creation failed") from exc

        try:
            payment = Payment(
                product_id=product.id,
                razorpay_order_id=order["id"],
                amount=amount_paise,
                currency=order.get("currency", "INR"),
                status=order.get("status", "created"),
            )
            payment = await self.payments.add(payment)
            await self.session.commit()
            return payment
        except SQLAlchemyError as exc:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Database error while saving the payment") from exc

    async def list_payments(self):
        return await self.payments.list_all()

    async def get_payment(self, payment_id: int):
        payment = await self.payments.get_by_id(payment_id)
        if payment is None:
            raise HTTPException(status_code=404, detail=f"Payment {payment_id} was not found")
        return payment

    async def get_razorpay_order(self, order_id: str) -> dict[str, Any]:
        try:
            return await asyncio.to_thread(razorpay_client.order.fetch, order_id)
        except (BadRequestError, GatewayError, ServerError) as exc:
            raise HTTPException(status_code=502, detail=f"Razorpay could not fetch the order: {exc}") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Razorpay order retrieval failed") from exc
