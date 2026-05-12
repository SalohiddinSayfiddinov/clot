from fastapi import FastAPI
from app.api import auth, products
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from app.models.user import User, Address, PaymentCard, Wishlist
from app.models.product import Product, CartItem, Category

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clot E-Commerce API")

# Include your routers
app.include_router(auth.router)
app.include_router(products.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
