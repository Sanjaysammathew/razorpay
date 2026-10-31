from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> list[Product]:
        result = await self.session.scalars(select(Product).order_by(Product.id))
        return list(result.all())

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)
