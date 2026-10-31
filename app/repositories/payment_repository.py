from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, payment: Payment) -> Payment:
        self.session.add(payment)
        await self.session.flush()
        await self.session.refresh(payment)
        return payment

    async def list_all(self) -> list[Payment]:
        result = await self.session.scalars(select(Payment).order_by(Payment.id.desc()))
        return list(result.all())

    async def get_by_id(self, payment_id: int) -> Payment | None:
        return await self.session.get(Payment, payment_id)

    async def get_by_order_id(self, order_id: str) -> Payment | None:
        result = await self.session.scalars(
            select(Payment).where(Payment.razorpay_order_id == order_id)
        )
        return result.one_or_none()
