from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.product import Product, CartItem
from app.models.user import Wishlist, User
from app.core.security import get_current_user, get_optional_current_user
from app.schemas.product import CartItemOut, ProductOut, ProductCreate

router = APIRouter(prefix="/products", tags=["Inventory"])


@router.get("")
def get_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    gender: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    on_sale: bool = False,
    free_shipping: bool = False,
    sort: str = "newest",
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    query = db.query(Product)

    # 1. Filters
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if gender:
        query = query.filter(Product.gender == gender)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if on_sale:
        query = query.filter(Product.old_price > Product.price)
    if free_shipping:
        query = query.filter(Product.is_free_shipping == True)

    # 2. Sorting
    if sort == "newest":
        query = query.order_by(desc(Product.created_at))
    elif sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())

    products = query.all()

    wishlisted_ids = set()
    if current_user:
        wishlisted_ids = {
            item.product_id
            for item in db.query(Wishlist.product_id)
            .filter(Wishlist.user_id == current_user.id)
            .all()
        }

    results = []
    for p in products:
        product_data = ProductOut.model_validate(p)

        # LOGIC: If guest, it's None. If logged in, it's True/False.
        if current_user is None:
            product_data.is_wishlisted = None
        else:
            product_data.is_wishlisted = p.id in wishlisted_ids

        results.append(product_data)

    return results


@router.post("/create", response_model=ProductOut)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.patch("/{product_id}/update", response_model=ProductOut)
def update_product(product_id: int, update_data: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}/delete")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@router.post("/cart/add")
def add_to_cart(
    product_id: int,
    color: str,
    size: str,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Create the cart entry
    cart_item = CartItem(
        user_id=current_user.id,
        product_id=product_id,
        color=color,
        size=size,
        quantity=quantity,
    )
    db.add(cart_item)
    db.commit()
    return {"message": "Added to cart successfully"}


@router.get("/cart", response_model=List[CartItemOut])
def get_my_cart(current_user: User = Depends(get_current_user)):
    return current_user.cart_items


@router.patch("/cart/{cart_item_id}/quantity")
def update_cart_quantity(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    item.quantity = quantity
    db.commit()
    return {"message": "Quantity updated"}


@router.delete("/cart/{cart_item_id}/remove")
def remove_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
