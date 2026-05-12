from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.order import Order, OrderItem
from app.models.product import CartItem
from app.models.user import Address, User, PaymentCard
from app.utils.helpers import get_address_string
from typing import List, Optional
from app.schemas.order import OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=List[OrderOut])
def get_my_orders(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Order).filter(Order.user_id == current_user.id)

    if status:
        query = query.filter(Order.status.ilike(status))

    return query.order_by(Order.created_at.desc()).all()


@router.post("/checkout")
def checkout(
    address_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == current_user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    card = db.query(PaymentCard).filter(PaymentCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Payment card not found")
    card_ref = f"**** {card.card_number[-4:]}"

    # Calculate Costs
    subtotal = 0
    for item in cart_items:
        if item.product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {item.product_id} no longer exists.",
            )
    subtotal += item.product.price * item.quantity
    shipping = 8.0
    tax = 0.0
    total = subtotal + shipping + tax

    address_str = get_address_string(address_id, db)

    new_order = Order(
        user_id=current_user.id,
        subtotal=subtotal,
        shipping_cost=shipping,
        tax=tax,
        total_price=total,
        address=address_str,
        payment_method=card_ref,
        status="Processing",
    )

    db.add(new_order)
    db.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            price_at_purchase=item.product.price,
            color=item.color,
            size=item.size,
            quantity=item.quantity,
        )
        db.add(order_item)
        db.delete(item)

    db.commit()
    return {"message": "Order placed successfully", "order_id": new_order.id}


from fastapi import HTTPException


@router.post("/{order_id}/change-status")
def change_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["Processing", "Shipped", "Delivered", "Returned", "Canceled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        )

    order.status = status

    db.commit()
    db.refresh(order)

    return {"message": "Status changed successfully", "new_status": order.status}
