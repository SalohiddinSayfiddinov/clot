from pydantic import BaseModel
from typing import List, Optional


class StaticReview(BaseModel):
    user_name: str
    user_image: Optional[str] = None
    stars: int
    comment: str
    date: Optional[str] = None  # Or use datetime


class CategoryBase(BaseModel):
    name: str
    image_url: Optional[str] = None


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    is_free_shipping: bool
    gender: str
    colors: List[str]
    sizes: List[str]
    images: List[str]
    reviews: List[StaticReview]
    category_id: int

    is_wishlisted: Optional[bool] = None
    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    is_free_shipping: bool = False
    gender: str
    colors: List[str] = []
    sizes: List[str] = []
    images: List[str] = []
    category_id: int
    reviews: List[StaticReview] = []


class CartItemOut(BaseModel):
    id: int
    product_id: int
    color: str
    size: str
    quantity: int
    product: ProductOut

    model_config = {"from_attributes": True}
