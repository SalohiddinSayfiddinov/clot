from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    JSON,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    is_free_shipping = Column(Boolean, default=False)
    gender = Column(String)  # Man, Woman, Kids

    # Selection Lists
    colors = Column(JSON, default=[])  # ["Red", "Black"]
    sizes = Column(JSON, default=[])  # ["S", "M", "L"]
    images = Column(JSON, default=[])  # ["url1", "url2"]

    # Static Reviews List
    # Each item: {"user_name": "", "user_image": "", "stars": 5, "comment": "", "date": ""}
    reviews = Column(JSON, default=[])

    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # The specific selections made by the user
    color = Column(String)
    size = Column(String)
    quantity = Column(Integer, default=1)

    product = relationship("Product")
    user = relationship("User", back_populates="cart_items")