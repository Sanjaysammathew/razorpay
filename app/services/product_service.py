from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductRepository(session)

    async def list_products(self):
        return await self.repository.list_all()

    async def get_product(self, product_id: int):
        return await self.repository.get_by_id(product_id)
