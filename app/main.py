from fastapi import FastAPI
from app.api import auth, categories, products, order, user
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clot E-Commerce API")

# Include your routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(order.router)
app.include_router(user.router)


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


# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc4NjgxMjI3fQ.WGomwu9f1SEWAJKFHbHI1WOkeZRsGJNNVNeVD72OY_w
