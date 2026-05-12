from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    addresses = relationship("Address", back_populates="user")
    cards = relationship("PaymentCard", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    wishlist_items = relationship("Wishlist", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")


class PaymentCard(Base):
    __tablename__ = "payment_cards"
    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    ccv = Column(String, nullable=False)
    exp = Column(String, nullable=False)
    cardholder_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="cards")


class Wishlist(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product")
