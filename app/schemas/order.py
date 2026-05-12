from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemOut(BaseModel):
    product_id: int
    price_at_purchase: float
    color: str
    size: str
    quantity: int
    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    total_price: float
    status: str
    address: str
    created_at: datetime
    items: List[OrderItemOut]

    model_config = {"from_attributes": True}
