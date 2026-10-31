from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.product_schema import ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductResponse])
async def list_products(session: AsyncSession = Depends(get_db)):
    return await ProductService(session).list_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: AsyncSession = Depends(get_db)):
    product = await ProductService(session).get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} was not found")
    return product
