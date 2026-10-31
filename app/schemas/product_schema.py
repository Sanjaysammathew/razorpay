from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
