from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    subtotal = Column(Float, nullable=False)
    shipping_cost = Column(Float, default=8.0)
    tax = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)

    status = Column(String, default="Pending")
    address = Column(String)
    payment_method = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # We save these explicitly in case the product changes later
    price_at_purchase = Column(Float, nullable=False)
    color = Column(String)
    size = Column(String)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
