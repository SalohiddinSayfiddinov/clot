from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    image_url: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
