from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import engine
from app.models import Base  # Import models so metadata is registered.
from app.routers.payment_router import router as payment_router
from app.routers.product_router import router as product_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenient for this learning project; production projects should use migrations.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Razorpay Test Payments API", version="1.0.0", lifespan=lifespan)
app.include_router(product_router)
app.include_router(payment_router)
